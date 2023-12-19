from flask import Flask, session, request
from flask_cors import CORS
from flask_socketio import SocketIO
from .models import db
from config import Config
from redis import Redis


app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object(Config)
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
connected_users = []

with app.app_context():
    db.create_all()


redis = Redis.from_url(app.config["REDIS_URL"])

@app.before_request
def before_request():
    if request.path.startswith("/api"):
        if 'prev_route' not in session:
            session['prev_route'] = ['main', '']
            session['curr_route'] = session['prev_route']
        else:
            session['prev_route'] = session['curr_route']
    elif not request.path.startswith("/static"):
        if 'curr_route' not in session:
            session['curr_route'] = []
            session['curr_route'].append(request.endpoint)
            session['curr_route'].append(request.query_string.decode('utf-8'))
            session['prev_route'] = session['curr_route']
        else:
            session['prev_route'] = session['curr_route']
            session['curr_route'] = []
            session['curr_route'].append(request.endpoint)
            session['curr_route'].append(request.query_string.decode('utf-8'))

from app.api import accept_friend, friendships, invite_friend, refresh_chat
from app.api import cancel_friend, get_username, send_message, conversations
from app.api import read_message, users
from app import routes, sockets


app.redis = redis
