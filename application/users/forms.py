from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,BooleanField,TextAreaField,ValidationError,Form,FileField
from wtforms.validators import DataRequired,Regexp,EqualTo,Length
from application.models import User

#=========== Sign up form for creating new accounts =============
class SignupForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters, numbers, dots or underscores')])
    password=PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password',message='Passwords didn\'t match')])
    confirm_password=PasswordField('Confirm Password', validators=[DataRequired()])
    # recaptcha = RecaptchaField()
    submit = SubmitField('Create Account')

    def validate_username(self,username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('Username already taken')


#=========== Login form for signing into the user accounts =============
class LoginForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

#=========== Form for updating the passwords =============
class UpdatePasswordForm(FlaskForm):
    old_password=PasswordField('Old password', validators=[DataRequired()])
    new_password=PasswordField('New password', validators=[DataRequired(),EqualTo('confirm_new_password',message='Passwords didn\'t match.')])
    confirm_new_password=PasswordField('Confirm New password', validators=[DataRequired()])
    submit=SubmitField('Update Password')

#=========== Form for uploading the profile pictures =============
class ImageForm(Form):
    profile=FileField('Upload Profile Image')
    submit=SubmitField('Update')
