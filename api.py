from flask_restful import Api,Resource,marshal_with,reqparse,fields,abort
from application.models import User,Posts
from application.utility import find_followers_of,find_following_of
from application import db
from flask import jsonify, make_response
from werkzeug.exceptions import HTTPException
import json

class BusinessValidationError(HTTPException):
    def __init__(self,status_code,error_code,error_message):
        message={"error_code":error_code,"error_message":error_message}
        self.response=make_response(json.dumps(message),status_code)

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, help='Username for the new User')
user_parser.add_argument('password', type=str, help='Password for the new User')

blog_parser = reqparse.RequestParser()
blog_parser.add_argument('title', type=str, help='Title')
blog_parser.add_argument('description', type=str, help='Description')

user_fields = {
    'user_id':   fields.Integer,
    'username':   fields.String,
    'follower_count':    fields.Integer,
    'following_count':    fields.Integer,
    'post_count':    fields.Integer,
    'account_created':    fields.DateTime
}

blog_fields = {
    'post_id':   fields.Integer,
    'title':   fields.String,
    'description':    fields.String,
    'image_url':    fields.String,
    'created_timestamp':    fields.String,
    'last_edited_timestamp':    fields.String,
    'author_id':    fields.Integer,
    'hidden':    fields.Integer,
    'likes_count':    fields.Integer
}

def forbidden(message,status_code=403):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = status_code
    return response    

def abort_if_user_doesnt_exist(user):
    if user is None:
        abort(404, message="User doesn't exist")

def abort_if_blog_doesnt_exist(blog):
    if blog is None:
        abort(404, message="Blog doesn't exist")

class UserApi(Resource):
    @marshal_with(user_fields)
    def get(self,user_id):
        user=User.query.filter_by(user_id=user_id).first()
        abort_if_user_doesnt_exist(user)
        return user
    
    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        username=args.get("username",None)
        password=args.get("password",None)
        if username is None:
            raise BusinessValidationError(status_code=400,error_code='USER001',error_message='username is required')
        if password is None:
            raise BusinessValidationError(status_code=400,error_code='USER002',error_message='password is required')
        user=User.query.filter_by(username=username).first()
        if user is not None:
            raise BusinessValidationError(status_code=400,error_code='USER003',error_message='username already taken')
        user=User(username=username,password=password)
        db.session.add(user)
        db.session.commit()
        return user

    @marshal_with(user_fields)
    def put(self):
        args = user_parser.parse_args()
        username=args.get("username",None)
        if username is None:
            raise BusinessValidationError(status_code=400,error_code='USER001',error_message='username is required')
        user=User.query.filter_by(username=username).first()
        abort_if_user_doesnt_exist(user)
        user.password=args.get("password",None)
        db.session.commit()
        return user

    def delete(self,user_id):
        user=User.query.filter_by(user_id=user_id).first()
        abort_if_user_doesnt_exist(user)
        for post in user.posts:
            db.session.delete(post)
        user_list=User.query.all()
        for follower in find_followers_of(user,user_list=user_list):
            follower.following_count-=1
        for following in find_following_of(user,user_list=user_list):
            following.follower_count-=1
        for follow in user.followed:
            db.session.delete(follow)
        for follow in user.followers:
            db.session.delete(follow)
        for comment in user.comments:
            db.session.delete(comment)
        for like in user.likes:
            post=Posts.query.filter_by(post_id=like.post_id).first()
            db.session.delete(like)
            post.compute_likes()
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message":"Successfully Deleted"})


class BlogApi(Resource):
    @marshal_with(blog_fields)
    def get(self,blog_id):
        blog=Posts.query.filter_by(post_id=blog_id).first()
        abort_if_blog_doesnt_exist(blog)
        if blog.hidden:
            forbidden("Blog is archived")
        blog=Posts.query.filter_by(post_id=blog_id).first()
        return blog

    @marshal_with(blog_fields)
    def post(self,user_id):
        args = blog_parser.parse_args()
        title=args.get("title",None)
        description=args.get("description",None)
        if title is None:
            raise BusinessValidationError(status_code=400,error_code='BLOG001',error_message='title is required')
        if description is None:
            raise BusinessValidationError(status_code=400,error_code='BLOG001',error_message='description is required')
        user=User.query.filter_by(user_id=user_id).first()
        abort_if_user_doesnt_exist(user)
        blog=Posts(title=title,description=description,author_id=user_id)
        user.posts.append(blog)
        user.post_count+=1
        db.session.add(blog)
        db.session.commit()
        return blog

    @marshal_with(blog_fields)
    def put(self,blog_id):
        blog=Posts.query.filter_by(post_id=blog_id).first()
        abort_if_blog_doesnt_exist(blog)
        args = blog_parser.parse_args()
        blog.title=args.get("title",None)
        blog.description=args.get("description",None)
        db.session.commit()
        return blog

    @marshal_with(blog_fields)
    def delete(self,blog_id):
        blog=Posts.query.filter_by(post_id=blog_id).first()
        abort_if_blog_doesnt_exist(blog)
        user=blog.author
        print(user)
        user.posts.remove(blog)     
        user.post_count-=1
        db.session.delete(blog)
        db.session.commit()
        return blog


class FeedApi(Resource):
    def get(self,user_id):
        user=User.query.filter_by(user_id=user_id).first()
        abort_if_user_doesnt_exist(user)
        all_posts=Posts.query.order_by(Posts.created_timestamp.desc())
        feed={}
        for post in all_posts:
            if post.author.is_followed_by(user) and post.hidden==False:
                feed[post.post_id]=post.to_json()
        return jsonify(feed)
