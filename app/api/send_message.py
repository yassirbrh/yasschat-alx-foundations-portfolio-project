from app import app
from flask import session, jsonify, request
from ..models import Message, db, User
from datetime import datetime


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

            # Add receiver's UserID to the Redis set
            app.redis.sadd('usersToRefresh', receiver.UserID)
            # Add sender's UserID to the Redis set
            app.redis.sadd('usersToRefresh', sender_id)

        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
