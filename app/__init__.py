from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_socketio import SocketIO
from settings import CHAT_DATABASE_URI

socketio = SocketIO()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = CHAT_DATABASE_URI
# Takes the CHAT_DATABASE_URI from environement
# and create a database engine
db = SQLAlchemy(app)


# Creates a model in database
# Access these fields from shell
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    is_active = db.Column(db.Boolean, unique=False, default=False)
    confirmed_email = db.Column(db.Boolean, unique=False, default=False)
    usernames = db.relationship('Group_user', backref='owner', lazy='dynamic')


# Creates a model in database
# for the grouo chat and keep
# record for all users chatting
class Group(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True, unique=False)
    group = db.Column(db.String(15), unique=False)
    username = db.Column(db.String(15))


# Cretes a model in database for
# private_chat. keep record of
# indivual details from whom they are
# chatting using id
class Group_user(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.String(15), unique=False)
    user2 = db.Column(db.String(15), db.ForeignKey('user.username'))


# Creates flask app
def create_app(debug=False):
    app.debug = debug
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app
