from app import app
from flask import session, jsonify, render_template, url_for, redirect, request
from ..models import db, Message


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
