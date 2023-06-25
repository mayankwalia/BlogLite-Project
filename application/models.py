import datetime
from flask_login import AnonymousUserMixin,UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from application import db,login_manager

#=========== Converting user_id to user object which will be stored in g.user  =============
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ============= Follow Model =============
class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
    primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
    primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

# ============= User Model =============
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), unique=True,nullable=False)
    bio=db.Column(db.Text)
    hashed_password = db.Column(db.String(255),nullable=False)
    # active = db.Column(db.Boolean(),default=True)
    follower_count=db.Column(db.Integer,default=0,nullable=False)
    # ============= following_count is optional =============
    following_count=db.Column(db.Integer,default=0,nullable=False)

    # ============= User - Follow/Following/Followed By - User (Relationship) =============
    followed = db.relationship('Follow',foreign_keys=[Follow.follower_id],backref=db.backref('follower', lazy='joined'),lazy='dynamic', cascade='all, delete-orphan')
    followers = db.relationship('Follow',foreign_keys=[Follow.followed_id],backref=db.backref('followed', lazy='joined'),lazy='dynamic', cascade='all, delete-orphan')
    # ============= Total Blogs created by the user =============
    post_count=db.Column(db.Integer,default=0,nullable=False)
    # ============= Date and Time when the user joined the BlogLite =============
    account_created=db.Column(db.DateTime,default=datetime.datetime.now)
    # ============= String stroring the filename of the profile picture (or store the default one) =============
    profile_image=db.Column(db.String,default='default_profile.jpg')
    # ============= List of all Blogs objects created by the user =============
    posts=db.relationship("Posts",backref="author")
    # ============= List of all Likes objects created by the user =============
    likes=db.relationship('Likes',backref='user')
    # ============= List of all Comment objects created by the user =============
    comments=db.relationship('Comments',backref='users')
    # ============= Plain password cannot be accessed =============
    @property
    def password(self):
        return AttributeError('Password is not readable')

    # ============= Storing Hashed password instead of plain text. Automatically called when user objectis created. =============
    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def get_id(self):
        return self.user_id

    # ============= Helper function for finding is one user is following another user or not =============
    def is_following(self, user):
        if (not user) or (user.user_id is None):
            return False
        return self.followed.filter_by(followed_id=user.user_id).first() is not None

    # ============= Helper function for finding is one user is being followed by another user or not =============
    def is_followed_by(self, user):
        if (not user) or (user.user_id is None):
            return False
        return self.followers.filter_by(follower_id=user.user_id).first() is not None

    # ============= Follow another user if this user is not already following and update the following and followers of the users =============
    def follow(self, user):
        if not self.is_following(user):
            follow_object = Follow(follower=self, followed=user)
            db.session.add(follow_object)
            self.following_count+=1
            user.follower_count+=1
            db.session.commit()
    # ============= Unfollow another user if this user is following another user and update the following and followers of the users =============    
    def unfollow(self, user):
        already_following = self.followed.filter_by(followed_id=user.user_id).first()
        if already_following:
            self.following_count-=1
            user.follower_count-=1
            db.session.delete(already_following)
            db.session.commit()
            
    # ====== Mainly for API ======
    def to_json(self):
        user = {
        'user_id':   self.user_id,
        'username':   self.username,
        'follower_count':    self.follower_count,
        'following_count':    self.following_count,
        'post_count':    self.post_count,
        'account_created':    self.account_created
        }
        return user

# ============= Optional =============    
# Can create Tags Model for blogs (many to many)

# ============= Posts/Blogs Model =============
class Posts(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_url = db.Column(db.String,default='default_blogpost.png')
    created_timestamp = db.Column(db.DateTime,default=datetime.datetime.now)
    last_edited_timestamp = db.Column(db.DateTime,default=datetime.datetime.now,onupdate=datetime.datetime.now)

    # ============= user_id of the author (who created this blog) =============
    author_id=db.Column(db.Integer,db.ForeignKey('users.user_id'),nullable=False)

    # ============= For archiving the blog post =============
    hidden=db.Column(db.Boolean,default=False)

    # ============= Likes count and list of likes objects for this Blog post =============
    likes_count = db.Column(db.Integer,nullable=False,default=0)
    likes=db.relationship('Likes',backref='post')

    # ============= List of comments objects for this Blog post =============
    comments=db.relationship('Comments',backref='posts')

    def __repr__(self):
        return '<Blog post: %s>' %self.title

    # ============= For updating likes when ever someone likes a blog =============
    def compute_likes(self):
        self.likes_count=len(self.likes)

    def compute_comments(self):
        return len(self.comments)

    # ============= Returns author in the form of user object =============
    def author(self):
        user=User.query.filter_by(author_id=self.author_id).first()
        return user
    
    # ====== Mainly for API ======
    def to_json(self):
        blog = {
        'post_id':   self.post_id,
        'title':   self.title,
        'description':    self.description,
        'image_url':    self.image_url,
        'created_timestamp':    self.created_timestamp,
        'last_edited_timestamp':    self.last_edited_timestamp,
        'author_id':    self.author_id,
        'hidden':    self.hidden,
        'likes_count':    self.likes_count
        }
        return blog


# ============= Comments Model =============
class Comments(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))
    comment_body = db.Column(db.Text())
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'))
    created_timestamp = db.Column(db.DateTime,default=datetime.datetime.now)
    last_edited_timestamp = db.Column(db.DateTime,default=datetime.datetime.now,onupdate=datetime.datetime.now)
    # Follow up -> Likes and Nested Comments?

    def __repr__(self):
        return '<Comment post: %s>' %self.comment_body

    # ============= Returns author in the form of user object =============
    def author(self):
        user=User.query.filter_by(user_id=self.user_id).first()
        return user
        

# ============= Likes Model =============
class Likes(db.Model):
    __tablename__ = 'likes'
    like_id=db.Column(db.Integer,primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))
    user_id=db.Column(db.String(100), db.ForeignKey('users.user_id'))

    def __repr__(self):
        return '<Like : %d>' %self.like_id

# ============= Anonymous User =============
class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.username = 'Guest'