from application import create_app, db
from flask import g,request, jsonify,render_template
from flask_login import current_user
from api import *

# ====== Creating app instance ===========
app=create_app()

# ====== Creating api instance and addding resources ===========
api=Api(app)
api.add_resource(UserApi,'/api/user','/api/user/<int:user_id>')
api.add_resource(BlogApi,'/api/blog/<int:blog_id>','/api/user/<int:user_id>/blog')
api.add_resource(FeedApi,'/api/feed/<int:user_id>')

# ====== Error Handlers for application and api ===========
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# ====== Storing the current user in the session ===========
@app.before_request
def before_request():
    g.user=current_user

# ====== Rendering home page ===========
@app.route("/", methods=["GET"])
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)