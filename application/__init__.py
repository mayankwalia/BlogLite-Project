from flask import Flask
from configuration import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_uploads import configure_uploads,UploadSet, IMAGES (Tried but there is some issue with werkzeug)

db = SQLAlchemy()

login_manager=LoginManager()

#=========== If user is not logged in display login page with message =============
login_manager.login_view="users.login"
login_manager.login_message = "Login required to access that content"
login_manager.login_message_category = "info"

def create_app():
    app=Flask(__name__)
    #=========== Using values from the configuration object for configuring application =============
    app.config.from_object(Configuration) 
    db.init_app(app)
    login_manager.init_app(app)

    
    #=========== Registering blueprints =============
    from application.users import users as user_blueprint
    app.register_blueprint(user_blueprint,url_prefix='/users')
    from application.posts import posts as post_blueprint
    app.register_blueprint(post_blueprint,url_prefix='/posts')

    
    #=========== Creating database if not available =============
    from application.models import User,Posts,Comments,Likes
    with app.app_context():
        db.create_all()
    return app
