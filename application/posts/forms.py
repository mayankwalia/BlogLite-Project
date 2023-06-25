from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField

#=========== Form for creating a new post =============
class PostForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired(message="Title is required")])
    description=StringField('Description',validators=[DataRequired()])
    image=FileField('Image')
    submit=SubmitField('Create')

#=========== Form for writing comment on a post  =============
class CommentForm(FlaskForm):
    comment=StringField('Body',validators=[DataRequired()])
    submit=SubmitField('Comment')