from app import app
from flask import session, request, redirect, url_for, jsonify
from ..models import db, User, Friendship


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
