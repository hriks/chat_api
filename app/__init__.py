from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_socketio import SocketIO


socketio = SocketIO()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bqlxjind:OtFzlf08n1g8WLnLd7vPFoHGB3DFGkcd@pellefant.db.elephantsql.com:5432/bqlxjind' # noqa
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    is_active = db.Column(db.Boolean, unique=False, default=False)
    usernames = db.relationship('Group', backref='owner', lazy='dynamic')


class Group(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(15), unique=False)
    username = db.Column(db.String(15), db.ForeignKey('user.username'))


class Group_user(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(15), unique=False)
    username = db.Column(db.String(15), db.ForeignKey('user.username'))


def create_app(debug=False):
    app.debug = debug
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app
