from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import data_required

class LoginForm(FlaskForm):
    username = StringField("username", validators=[data_required()])
    password = PasswordField("password", validators=[data_required()])
    remember_me = BooleanField("remember_me")

    