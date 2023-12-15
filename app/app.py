#!/usr/bin/python3
'''
    This is the entry point of the application
'''
from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask import jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import secrets
from models.User import db, User
from models.Friendship import Friendship
from models.Message import Message
from datetime import datetime
from sqlalchemy import or_, and_, desc
#from flask_sse import sse

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Yassir2001@localhost:3306/YassChat'
#app.config['SESSION_COOKIE_SECURE'] = True
#app.config['SESSION_COOKIE_HTTPONLY'] = False
#app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config["REDIS_URL"] = "redis://localhost"
#app.register_blueprint(sse, url_prefix='/stream_data')
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
connected_users = []
usersToRefresh = []

@app.before_request
def before_request():
    if request.path.startswith("/api"):
        if 'prev_route' not in session:
            session['prev_route'] = ['main', '']
            session['curr_route'] = session['prev_route']
        else:
            session['prev_route'] = session['curr_route']
    elif not request.path.startswith("/static"):
        if 'curr_route' not in session:
            session['curr_route'] = []
            session['curr_route'].append(request.endpoint)
            session['curr_route'].append(request.query_string.decode('utf-8'))
            session['prev_route'] = session['curr_route']
        else:
            session['prev_route'] = session['curr_route']
            session['curr_route'] = []
            session['curr_route'].append(request.endpoint)
            session['curr_route'].append(request.query_string.decode('utf-8'))


# Define the routes
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('main'))
    return render_template('index.html')

@app.route('/signup')
def signup():
    if 'username' in session:
        return redirect(url_for('main'))
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def handle_signup():
    if request.method == 'POST':
        username = request.form['username']
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confpassword']

        # Check if username is already used
        if User.query.filter_by(Username=username).first():
            flash('Username already in use. Please choose another.', 'error')
            return redirect(url_for('signup'))

        # Check if email is already used
        if User.query.filter_by(Email=email).first():
            flash('Email already in use. Please use another email.', 'error')
            return redirect(url_for('signup'))

        # Check if password and its confirmation match
        if password != confirm_password:
            flash('Password and confirmation do not match. Please try again.', 'error')
            return redirect(url_for('signup'))

        new_user = User(
                Username=username,
                FullName=fullname,
                Email=email,
                Password=password
                )

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. You can now log in!', 'success')
        return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/login')
def login():
    if 'username' in session:
        return redirect(url_for('main'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def handle_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not User.query.filter_by(Username=username).first():
            flash('Invalid username.', 'error')
        else:
            if not User.query.filter_by(Username=username, Password=password).first():
                flash('Password incorrect.', 'error')
            else:
                user = User.query.filter_by(Username=username, Password=password).first()
                session['user_id'] = user.UserID
                session['username'] = user.Username
                session['fullname'] = user.FullName
                session['email'] = user.Email
                return redirect(url_for('main'))
        return redirect(url_for('login'))

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

'''
@app.route('/stream_data')
def stream_data():
    return sse.stream()
'''

@app.route('/api/read-message', methods=['POST'])
def handle_read_message():
    data = request.get_json()
    message_ids = data.get('messageIDs', [])
    prev_route = session['prev_route'][0]
    query = session['prev_route'][1]

    try:
        # Update the isRead field to True for the specified message IDs
        Message.query.filter(Message.MessageID.in_(message_ids)).update(
            {Message.isRead: True},
            synchronize_session=False
        )
        # Commit the changes to the database
        db.session.commit()

        return redirect(url_for(prev_route) + '?' + query)

    except Exception as e:
        # Handle any exceptions or errors
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/send-message', methods=['POST'])
def send_message():
    try:
        sender_id = session.get('user_id')
        data = request.get_json()
        destination_username = data.get('to')
        receiver = User.query.filter_by(Username=destination_username).first()
        prev_route = session['prev_route'][0]
        query = session['prev_route'][1]

        if sender_id and receiver:
            new_message = Message(
                SenderID=sender_id,
                ReceiverID=receiver.UserID,
                Message=data.get('message'),
                Timestamp=datetime.now(),
                isRead=False
            )

            db.session.add(new_message)
            db.session.commit()

            # Use the receiver's user ID as the room identifier
            room = str(receiver.UserID)

            # Emit a message to the specific user's room using Flask-SocketIO
            usersToRefresh.append(receiver.UserID)
            usersToRefresh.append(sender_id)

        return jsonify({'status': 'success'})

    except Exception as e:
        print(f"Error handling send message: {str(e)}")
        import traceback
        traceback.print_exc()  # Print the full traceback
        return jsonify({'status': 'error', 'message': str(e)}), 500



@app.route('/api/users', methods=['GET'])
def get_all_usernames():
    try:
        # Query all usernames from the User table
        search_pattern = request.args.get('query', '')
        if len(search_pattern) == 0:
            usernames = [user.Username for user in User.query.all()]
        else:
            query = User.query.filter(User.Username.startswith(search_pattern))
            usernames = [user.Username for user in query]
        return jsonify(usernames)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/debug/session')
def debug_session():
    # Convert session variables to a dictionary for JSON response
    session_variables = dict(session)
    return jsonify(session_variables)


@app.route('/search')
def search_results():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    query = request.args.get('query', '')
    if len(query) != 0:
        return render_template('search.html', query=query)
    return render_template('search.html')


@app.route('/api/cancel-friend', methods=['GET'])
def cancelFriend():
    friendshipid = request.args.get('query', '')
    if 'user_id' not in session or not friendshipid:
        return redirect(url_for('index'))
    userid = session['user_id']
    user = User.query.filter_by(UserID=userid).first()
    prev_route = session['prev_route'][0]
    query = session['prev_route'][1]
    friend = Friendship.query.filter_by(FriendshipID=friendshipid).first()
    if not friend:
        return jsonify({'error': 'Friendship not found'}), 404
    # Check if the user is the sender or receiver in the friendship
    if user.UserID == friend.UserID or user.UserID == friend.FriendID:
        Friendship.query.filter_by(FriendshipID=friendshipid).delete()
        db.session.commit()
    return redirect(url_for(prev_route) + '?' + query)

@app.route('/api/accept-friend', methods=['GET'])
def acceptFriend():
    friendship_id = request.args.get('query', '')
    if 'user_id' not in session or not friendship_id:
        return redirect(url_for('index'))
    user_id = session['user_id']
    user = User.query.filter_by(UserID=user_id).first()
    prev_route = session['prev_route'][0]
    query = session['prev_route'][1]
    friend = Friendship.query.filter_by(FriendshipID=friendship_id).first()
    if not friend:
        return jsonify({'error': 'Friendship not found'}), 404
    # Check if the user is the sender or receiver in the friendship
    if user.UserID == friend.UserID or user.UserID == friend.FriendID:
        friend.isAccepted = True  # Set isAccepted to True instead of deleting the row
        db.session.commit()
    return redirect(url_for(prev_route) + '?' + query)


@app.route('/api/invite-friend', methods=['GET'])
def inviteFriend():
    try:
        if 'user_id' not in session:
            return redirect(url_for('index'))
        query = session['prev_route'][1]
        session.pop('query', None)
        friend = request.args.get('friend', '')
        username = session['username']
        inviter = User.query.filter_by(Username=username).first()
        receiver = User.query.filter_by(Username=friend).first()
        prev_route = session['prev_route'][0]

        # Check if both users exist
        if inviter and receiver:
            # Create a friendship invitation with isAccepted set to NULL
            friendship_invitation = Friendship(user_id=inviter.UserID, friend_id=receiver.UserID, is_accepted=None)

            # Add the invitation to the database
            db.session.add(friendship_invitation)
            db.session.commit()
        return redirect(url_for(prev_route) + '?' + query)
    except Exception as e:
        print(f"Error for sending invitation: {str(e)}")
        return jsonify({'error': str(e)})


@app.route('/api/friendships', methods=['GET'])
def get_friendships():
    username = session.get('username')

    if not username:
        return jsonify({'error': 'Username not found in session'}), 401

    friendship_list = []

    friendships = Friendship.query.all()

    for friendship in friendships:
        sender = User.query.get(friendship.UserID)
        receiver = User.query.get(friendship.FriendID)

        if sender.Username == username or receiver.Username == username:
            is_online = None

            if friendship.isAccepted:
                sender_online = sender.Username in connected_users
                receiver_online = receiver.Username in connected_users

                if sender.Username == username and receiver_online:
                    is_online = True
                elif receiver.Username == username and sender_online:
                    is_online = True
                else:
                    is_online = False

            # Get Last_Active from the User table
            last_active = sender.Last_Active if sender.Username != username else receiver.Last_Active

            # Convert Last_Active to a more readable format if needed
            # For example, assuming Last_Active is a datetime object
            last_active_str = last_active.strftime("%Y-%m-%d %H:%M:%S")

            friendship_info = {
                'FriendshipID': friendship.FriendshipID,
                'SenderUsername': sender.Username,
                'ReceiverUsername': receiver.Username,
                'isAccepted': friendship.isAccepted,
                'isOnline': is_online,
                'Last_Active': last_active_str
            }

            friendship_list.append(friendship_info)

    return jsonify(friendship_list)


@app.route('/api/get-username', methods=['GET'])
def get_username():
    username = session.get('username')

    if username:
        return jsonify([username])
    else:
        return jsonify({'error': 'Username not found in session'}), 401

@app.route('/api/refresh-chat', methods=['GET'])
def refresh_chat():
    user_id = session.get('user_id')
    username = session.get('username')
    global usersToRefresh

    if user_id and username:
        if user_id in usersToRefresh and username in connected_users:
            value_to_remove = user_id
            usersToRefresh = [item for item in usersToRefresh if item != value_to_remove]
            return jsonify({'refresh': True})
        else:
            return jsonify({'refresh': False, 'message': 'User should not refresh the chat.'})

    return jsonify({'error': 'User ID or username not found in session.'}), 401


@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    try:
        # Get the user ID from the session
        user_id = session.get('user_id')

        # Find all unique user IDs (excluding the current user)
        messages = Message.query.filter(or_(Message.SenderID == user_id, Message.ReceiverID == user_id)).all()
        other_user_ids = set()

        for message in messages:
            if message.ReceiverID == user_id:
                other_user_ids.add(message.SenderID)
            else:
                other_user_ids.add(message.ReceiverID)

        # Prepare the result dictionary
        result = {'conversations': []}

        # Iterate through each unique user ID to organize messages into conversations
        for other_user_id in other_user_ids:
            # Get the other user's username
            other_username = User.query.get(other_user_id).Username

            # Find messages exchanged between the current user and the other user
            messages = Message.query.filter(
                or_(
                    and_(Message.SenderID == user_id, Message.ReceiverID == other_user_id),
                    and_(Message.SenderID == other_user_id, Message.ReceiverID == user_id)
                )
            ).all()

            # Sort messages by timestamp in ascending order (from older to newer)
            messages = sorted(messages, key=lambda x: x.Timestamp)

            # Format messages as needed
            formatted_messages = [
                {
                    'messageID': message.MessageID,
                    'message': message.Message,
                    'timestamp': message.Timestamp,
                    'type': 'sent' if message.SenderID == user_id else 'received',
                    'isRead': message.isRead
                } for message in messages
            ]

            # Append conversation details to the result
            result['conversations'].append({
                'other_user_id': other_user_id,
                'other_username': other_username,
                'messages': formatted_messages
            })

        # Sort conversations based on the timestamp of their last message in descending order
        result['conversations'] = sorted(
            result['conversations'],
            key=lambda conv: conv['messages'][-1]['timestamp'],
            reverse=True
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/main')
def main():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('main.html')


@app.route('/logout')
def logout():
    try:
        # Check if the user is logged in
        if 'user_id' in session:
            # Get the user ID
            user_id = session['user_id']

            # Update the Last_Active attribute in the User table
            user = User.query.filter_by(UserID=user_id).first()
            user.Last_Active = datetime.now()

            # Commit the changes to the database
            db.session.commit()

            # Remove user from the connected_users list
            '''
            if 'username' in session:
                connected_users.remove(session['username'])
            '''

            # Clear session data
            session.clear()

        return redirect(url_for('index'))

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(app, port=5000)
