from flask_sqlalchemy import SQLAlchemy
from flask import render_template,redirect,url_for,request,flash
from application.posts import posts
from application.posts.forms import PostForm,CommentForm
# from werkzeug.utils import secure_filename This is giving error
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from application.models import Posts,Likes,Comments
from application import db
import os
import uuid



# =============== CRUD on Blog ===============

# =============== Create Blog ===============
@posts.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = PostForm()
    if request.method=='POST' and form.validate_on_submit():
        newPost=Posts()
        newPost.title=request.form['title']
        newPost.description=request.form['description']
        newPost.author_id=current_user.user_id
        current_user.posts.append(newPost)
        current_user.post_count+=1

        blog_image = request.files['image']
        filename = secure_filename(blog_image.filename)
        if filename!='':
            prefix=str(uuid.uuid1())
            # For unique filenames
            newPost.image_url=prefix+filename
            blog_image.save(os.path.join('application/static/images/', newPost.image_url))
        else:
            newPost.image_url='default_blogpost.png'
        try:
            db.session.add(newPost)
            db.session.commit()
            flash('Blog created successfully!','success')
            return redirect(url_for('users.dashboard'))
        except:
            flash('OOPS! Some error occured...Try again','warning')
    return render_template('create_or_update_post.html', form=form,update=False)


# =============== Read Blog ===============
@posts.route("<int:post_id>", methods=["GET", "POST"])
def individual_post(post_id):
    post=Posts.query.filter_by(post_id=post_id).first_or_404()
    like=Likes.query.filter((Likes.post_id==post_id) & (Likes.user_id==current_user.user_id)).first()
    if like:
        liked=True
    else:
        liked=False
    return render_template('posts.html',post=post,liked=liked)

# =============== Update Blog ===============
@posts.route("/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit(post_id):
    form = PostForm()
    post=Posts.query.filter_by(post_id=post_id).first_or_404()
    if request.method=='POST' and form.validate_on_submit():
        post.title=request.form['title']
        post.description=request.form['description']
        post.author_id=current_user.user_id
        updated_blog_image = request.files['image']
        if updated_blog_image:
            filename = secure_filename(updated_blog_image.filename)
            prefix=str(uuid.uuid1())
            post.image_url=prefix+filename
            updated_blog_image.save(os.path.join('application/static/images/', post.image_url))
        elif 'remove' in request.form:
            post.image_url='default_blogpost.png'
        try:
            db.session.commit()
            flash('Blog updated successfully!','success')
            return redirect(url_for('users.dashboard'))
        except:
            flash('OOPS! Some error occured while updating Blog...Try again','warning')
    form.title.data=post.title
    form.description.data=post.description
    return render_template('create_or_update_post.html', form=form,post_id=post_id,update=True)

# =============== Delete Blog ===============
@posts.route("/delete/<int:post_id>", methods=["GET", "POST"])
@login_required
def delete(post_id):
    post=Posts.query.filter_by(post_id=post_id).first_or_404()
    if current_user==post.author:
        try:
            current_user.posts.remove(post)
            current_user.post_count-=1
            db.session.delete(post)
            db.session.commit()
            flash('Blog removed successfully!','success')
            return redirect(url_for('users.dashboard'))
        except Exception as e:
            flash('OOPS! Some error occured while removing Blog...Try again','warning')
    else:
        flash('Premission Denied! You are not author of this blog.','danger')
    return redirect(url_for('users.dashboard'))
    

# =============== Optional Requirement ===============
# =============== Archiving Blog ===============
@posts.route("/archive/<int:post_id>", methods=["GET", "POST"])
@login_required
def archive_post(post_id):
    personal=request.args.get('personal')
    post=Posts.query.filter_by(post_id=post_id).first_or_404()
    if post.author_id==current_user.user_id:
        post.hidden=not post.hidden
        db.session.commit()
    if personal:
        flash('Blog made public successfully','success')
        return redirect(url_for('users.personal_dashboard'))
    flash('Blog archived successfully','success')
    return redirect(url_for('users.dashboard'))

# =============== Commenting on a Blog ===============
@posts.route("/comment/<int:post_id>", methods=["GET", "POST"])
def comment(post_id):
    post=Posts.query.filter_by(post_id=post_id).first_or_404()
    form=CommentForm()
    if request.method=='POST':
        if form.validate_on_submit():
            comment_body=form.comment.data
            comment=Comments(user_id=current_user.user_id,post_id=post_id,comment_body=comment_body)
            db.session.add(comment)
            db.session.commit()
            flash('Comment added successfully.',category='success')
            return redirect(url_for('posts.individual_post',post_id=post_id))
        else:
            flash('Some error occurred...Try again.',category='danger')
    return render_template('comment.html',form=form,post=post)
