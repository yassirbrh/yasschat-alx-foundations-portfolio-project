from app import app
from flask import session, jsonify


@app.route('/api/get-username', methods=['GET'])
def get_username():
    username = session.get('username')

    if username:
        return jsonify([username])
    else:
        return jsonify({'error': 'Username not found in session'}), 401
