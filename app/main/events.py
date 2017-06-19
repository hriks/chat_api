from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio


# when a private_chat is called, this method get
# token from sessio['room'] and based on token
# message is send
@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit(
        'status', {
            'msg': session.get('name') + ' has entered the room.'
        }, room=room
    )


# when a user enter the messages or text someone in the
# chat_box this method is called
@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit(
        'message', {
            'msg': session.get('name') + ':' + message['msg']
        }, room=room
    )


# This is called when a user closes the chatbox
# pop method is called along with this method
@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit(
        'status', {
            'msg': session.get('name') + ' has left the room.'
        }, room=room
    )
