import os
basedir = os.path.dirname(os.path.realpath(__file__))

class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI=f'sqlite:///{basedir}/testdb.db'
    # ====== Can be read from environment variables, but to avoid complexity I have hardcoded ===========
    SECRET_KEY = 'somethingsecure'
    TEMPLATES='application/templates'
    UPLOAD_FOLDER= 'application/static/images/'
    ENGAGEMENT= 'application/static/engagement_data/'

    