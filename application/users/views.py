from flask import render_template,redirect,url_for,request,flash,send_file
from application.users import users
from application.users.forms import SignupForm,LoginForm,UpdatePasswordForm,ImageForm
from application.models import User,Posts,Likes
from werkzeug.utils import secure_filename
from application import db
import os
from flask_login import login_required,login_user,logout_user,current_user
from application.utility import find_followers_of,find_following_of,get_user_from_id

# ===================== Displaying all users ===============
# =============== Used for displaying following and followers of every users when clicked on Search or Profile page ===============
@users.route("/", methods=["GET", "POST"])
@login_required
def users_listing():
    list_type=request.args.get('type')
    user_id=request.args.get('user')
    if user_id:
        user=get_user_from_id(int(user_id))
    user_list=User.query.all()
    # following is used for showing correct button Follow/Unfollow in front of the users
    following=find_following_of(current_user,user_list)
    # If clicked on follower count of any user then it should display all followers of that user along with info whether the current_user is following them or not
    if list_type=='Followers':
        users=find_followers_of(user,user_list)
    # When clicked on following count
    elif list_type=='Following':
        users=find_following_of(user,user_list)
    else:
        users=user_list
    return render_template('search_users.html',users=users,following=following)




# =============== Public profile page of a User ===============
@users.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    dashboard_user_id=request.args.get('user')
    if dashboard_user_id is not None:
        dashboard_user=get_user_from_id(int(dashboard_user_id))
    else:
        dashboard_user=current_user
    return render_template('dashboard.html',user=dashboard_user,hidden=False)

# =============== Private profile page of a User containing archive blogs ===============
@users.route("/personaldashboard", methods=["GET", "POST"])
@login_required
def personal_dashboard():
    dashboard_user_id=request.args.get('user')
    if dashboard_user_id is not None:
        dashboard_user=get_user_from_id(int(dashboard_user_id))
    else:
        dashboard_user=current_user

    return render_template('dashboard.html',user=dashboard_user,archive=True)


@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('users.dashboard'))
        flash('Invalid username or password.',category='warning')
    return render_template('login.html', form=form)

@users.route("/signup", methods=["GET", "POST"])
def signup():
    form=SignupForm()
    if request.method=='POST':
        if form.validate_on_submit():
            username=form.username.data
            form.username.data=''
            password=form.password.data
            form.password.data=''
            new_user=User(username=username,password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('users.user_feed'))
        else:
            for error in form.errors.keys():
                flash(*form.errors[error],category='warning')
            return redirect(url_for('users.signup'))
    else:
        return render_template('signup.html',form=form)

@users.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash('Logged out successfully',category='success')
    return redirect(url_for('home'))


@users.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    for post in current_user.posts:
        db.session.delete(post)
    user_list=User.query.all()
    # Updating the followers, followings of other users
    for follower in find_followers_of(current_user,user_list=user_list):
        follower.following_count-=1
    for following in find_following_of(current_user,user_list=user_list):
        following.follower_count-=1
    for follow in current_user.followed:
        db.session.delete(follow)
    for follow in current_user.followers:
        db.session.delete(follow)
    # Removing the likes and comments made by this user
    for comment in current_user.comments:
        db.session.delete(comment)
    for like in current_user.likes:
        post=Posts.query.filter_by(post_id=like.post_id).first()
        db.session.delete(like)
        # post.compute_likes()
    # Finally deleting the user
    db.session.delete(current_user)
    db.session.commit()
    flash('Account deleted successfully',category='success')
    return redirect(url_for('home'))



@users.route('/update-password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Password updated successfully.',category='success')
            return redirect(url_for('users.dashboard'))
        else:
            flash('Invalid password...Try again!',category='danger')
    else:
        flash('Passwords didn\'t match...Try again!',category='danger')
    return render_template("update_password.html", form=form)


@users.route('/upload-image/',methods=['GET','POST'])
@login_required
def upload():
    if request.method=='POST':
        form=ImageForm(request.form)
        if form.validate():
            image=request.files['profile']
            if image:
                import random
                n=random.randint(1,10000)
                random_name=str(n)+secure_filename(image.filename)
                filename=os.path.join('application/static/images/',random_name)
                image.save(filename)
                flash(f'Profile picture updated successfully".','success')
                current_user.profile_image=random_name
            elif 'remove' in request.form:
                flash(f'Profile picture removed successfully".','success')
                current_user.profile_image='default_profile.jpg'
            bio=request.form.get("bio")
            if bio:
                flash(f'Bio updated successfully".','success')
                current_user.bio=bio
            db.session.commit()
            return redirect(url_for('users.dashboard'))
    else:
        form=ImageForm()
        form.bio=current_user.bio
    return render_template('update_profile.html',form=form)



@users.route("/feed/<int:post_id>", methods=["GET", "POST"])
def likes(post_id):
    next=request.args.get('next')
    post=Posts.query.filter_by(post_id=post_id).first()
    like=Likes.query.filter((Likes.post_id==post_id) & (Likes.user_id==current_user.user_id)).first()
    if like is None:
        db.session.add(Likes(post_id=post_id,user_id=current_user.user_id))
        flash('Post liked successfully','success')
        liked=True
    else:
        db.session.delete(like)
        flash('Post unliked successfully','success')
        liked=False
    post.compute_likes()
    db.session.commit()
    if next:
        return render_template(next,post=post,liked=liked)
    return redirect(url_for('users.user_feed'))

@users.route("/feed", methods=["GET", "POST"])
@login_required
def user_feed():
    user_list=User.query.all()
    feed_posts=[]
    all_posts=Posts.query.order_by(Posts.created_timestamp.desc())
    likes=Likes.query.filter_by(user_id=current_user.user_id)
    post_liked_ids=[like.post_id for like in likes]
    for post in all_posts:
        if post.author.is_followed_by(current_user) and post.hidden==False:            
            feed_posts.append(post)

    return render_template('feed.html',posts=feed_posts,likes=post_liked_ids)



@users.route("follow", methods=["GET"])
def follow():
    user_id=request.args.get('user')
    user=User.query.filter_by(user_id=user_id).first_or_404()
    current_user.follow(user)
    return redirect(url_for('users.users_listing'))



@users.route("unfollow", methods=["GET"])
def unfollow():
    user_id=request.args.get('user')
    user=User.query.filter_by(user_id=user_id).first_or_404()
    current_user.unfollow(user)
    return redirect(url_for('users.users_listing'))


@users.route("/search", methods=["GET"])
def search():
    keyword=request.args.get('query')
    # ======= Using regular expression and like
    query="%"+keyword+"%"
    results=User.query.filter(User.username.like(query)).all()
    return render_template('search_users.html',search_query=keyword,users=results)


@users.route("<username>/posts", methods=["GET"])
def user_posts(username):
    user=User.query.filter_by(username=username).first_or_404()
    return render_template('userposts.html',user=user,posts=[post for post in user.posts if post.hidden==False])

def generate_csv(only_data=False):
    import csv
    fields = ['Post Title', 'Post Description','Created','Last Edited','Archived', 'Likes Count', 'Comments Count']
    rows = [[post.title,post.description,post.created_timestamp.strftime("%Y-%m-%d %H:%M:%S"),post.last_edited_timestamp.strftime("%Y-%m-%d %H:%M:%S"),post.hidden,post.likes_count,len(post.comments)] for post in current_user.posts]
    data={'fields':fields,'rows':rows}
    if only_data:
        return data
    data_file=os.path.join('application/static/engagement_data/',f'user_{current_user.username}.csv')
    try:
        csvfile=open(data_file, 'w',newline='')
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)
        # writing the data rows
        csvwriter.writerows(rows)
        csvreader = csv.reader(csvfile, delimiter=',')
        return data_file
    except:
        flash('Some error occured. Try again later','danger')
        return False


@users.route("/engagement", methods=["GET"])
def engagement():  
    csv=generate_csv() 
    if csv:
        return send_file(f"{csv[12:]}",as_attachment=True)
    else:
        return redirect(url_for('users.dashboard'))

@users.route("/insights", methods=["GET"])
def insights():
    data=generate_csv(only_data=True)
    values=data["rows"]
    posts_title,archived,created,like_counts,comment_counts=[],[],[],[],[]
    for tit,desc,ct,et,arc,lc,cc in values:
        posts_title.append(tit[:7])
        created.append(ct)
        archived.append(arc)
        like_counts.append(lc)
        comment_counts.append(cc)
    barplot(posts_title,like_counts,comment_counts)
    return render_template('insights.html')


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def barplot(post_title,likes_count,comments_count):
    try:
        os.remove(f'application/static/engagement_data/{current_user.username}_likes_bar.png')
    except:
        pass
    try:
        os.remove(f'application/static/engagement_data/{current_user.username}_comments_bar.png')
    except:
        pass
    plt.bar(post_title,likes_count,width = 0.4)
    plt.xlabel("Posts")
    plt.ylabel("Likes Counts")
    plt.title("Like Engagement Chart")
    plt.savefig(f'application/static/engagement_data/{current_user.username}_likes_bar.png')
    plt.clf()
    plt.bar(post_title,comments_count,width = 0.4)
    plt.xlabel("Posts")
    plt.ylabel("Comment Counts")
    plt.title("Comment Engagement Chart")
    plt.savefig(f'application/static/engagement_data/{current_user.username}_comments_bar.png')



# ============ Routes for testing purposes ============
@users.route("404", methods=["GET"])
def test_404():
    return render_template('404.html')

@users.route("500", methods=["GET"])
def test_500():
    return render_template('500.html')