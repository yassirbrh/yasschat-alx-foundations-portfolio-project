from app import app
from flask import session, jsonify
from ..models import User, Message
from sqlalchemy import or_, and_, desc


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

