from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):

    username = StringField(label='username:', validators=[DataRequired()])
    password = PasswordField(label='password:', validators=[DataRequired()])
    submit = SubmitField(label='submit')

class ChangePswForm(FlaskForm):
    
    old_password = PasswordField(label='Old password:', validators=[DataRequired()])
    password = PasswordField(label='New password:', validators=[DataRequired()])
    cfm_password = PasswordField(label='Confirm password:', validators=[DataRequired()])
    submit = SubmitField(label='submit')
  

class DeleteUserForm(FlaskForm):

    submit = SubmitField(label='Confirm')


class LoginForm(FlaskForm):

    username = StringField(label='username:', validators=[DataRequired()])
    password = PasswordField(label='password:', validators=[DataRequired()])
    submit = SubmitField(label='login')
