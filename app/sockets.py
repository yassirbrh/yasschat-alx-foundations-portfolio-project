from app import socketio, connected_users
from flask_socketio import emit, join_room, leave_room
from flask import session
from .models import db, User
from datetime import datetime


@socketio.on('connect')
def handle_connect():
    if 'user_id' in session:
        user_id = session['user_id']

        # Leave the room named after the user's ID
        join_room(user_id)

        # Remove the username from the connected_users set
        if session['username'] not in connected_users:
            connected_users.append(session['username'])

        # Emit an event to inform others that the user has disconnected
        emit('user_connected', {'username': session['username']}, room=user_id, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    if 'user_id' in session:
        user_id = session['user_id']

        # Leave the room named after the user's ID
        leave_room(user_id)

        # Remove the username from the connected_users set
        if session['username'] in connected_users:
            connected_users.remove(session['username'])

        # Update the Last_Active attribute in the User table
        user = User.query.filter_by(UserID=user_id).first()
        user.Last_Active = datetime.now()

        # Commit the changes to the database
        db.session.commit()

        # Emit an event to inform others that the user has disconnected
        emit('user_disconnected', {'username': session['username']}, room=user_id)
