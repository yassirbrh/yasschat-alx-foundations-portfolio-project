from app import app
from flask import request, session, redirect, url_for, jsonify
from ..models import db, User, Friendship


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