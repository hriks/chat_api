from flask_wtf import Form

from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


# Login form. This is displayed when user
# tried to login
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


# Registration form. This is dislayed when a
# a Guest tries to registers
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


# This open the group form when user
# tries to create a new group
class GroupForm(Form):
    groupname = StringField(
        'Group Name', validators=[
            InputRequired(), Length(min=4, max=15)
        ]
    )
