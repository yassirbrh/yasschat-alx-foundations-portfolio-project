from app import app, connected_users
from flask import session, jsonify
from ..models import User, Friendship


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
