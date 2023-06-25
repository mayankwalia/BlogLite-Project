from application.models import User

def find_followers_of(user,user_list):
    followers=[]
    for u in user_list:
        if user.is_followed_by(u):
            followers.append(u)
    return followers

def find_following_of(user,user_list):
    following=[]
    for u in user_list:
        if u.is_followed_by(user):
            following.append(u)
    return following

def get_user_from_id(id):
    return User.query.filter_by(user_id=id).first_or_404()