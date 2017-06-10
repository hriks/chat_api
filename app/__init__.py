from flask import Flask
from flask_socketio import SocketIO


socketio = SocketIO()


app = Flask(__name__)


def create_app(debug=False):
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app
