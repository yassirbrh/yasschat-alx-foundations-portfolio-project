from app import app
from flask import session, request, redirect, url_for, jsonify
from ..models import db, User, Friendship


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
