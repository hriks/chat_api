from flask_wtf import Form

from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(Form):
    username = StringField(
        'username',
        validators=[InputRequired(), Length(min=4, max=15)]
    )
    password = PasswordField(
        'password',
        validators=[InputRequired(), Length(min=8, max=80)]
    )
    remember = BooleanField('remember me')


class RegisterForm(Form):
    email = StringField(
        'email', validators=[InputRequired(), Email(
            message='Invalid email'
        ), Length(max=50)]
    )
    username = StringField(
        'username', validators=[InputRequired(), Length(min=4, max=15)]
    )
    password = PasswordField(
        'password',
        validators=[InputRequired(), Length(min=8, max=80)]
    )


class GroupForm(Form):
    groupname = StringField(
        'Group Name', validators=[
            InputRequired(), Length(min=4, max=15)
        ]
    )
