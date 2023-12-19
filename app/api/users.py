from app import app
from flask import request, jsonify
from ..models import User


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

