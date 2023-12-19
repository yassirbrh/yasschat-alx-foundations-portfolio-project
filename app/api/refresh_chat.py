from app import app, connected_users
from flask import session, jsonify


@app.route('/api/refresh-chat', methods=['GET'])
def refresh_chat():
    user_id = session.get('user_id')
    username = session.get('username')

    if user_id and username:
        # Check if user_id is in the Redis set 'usersToRefresh'
        if app.redis.sismember('usersToRefresh', user_id):
            # Remove user_id from the Redis set
            app.redis.srem('usersToRefresh', user_id)
            return jsonify({'refresh': True})
        else:
            return jsonify({'refresh': False, 'message': 'User should not refresh the chat.'})

    return jsonify({'error': 'User ID or username not found in session.'}), 401
