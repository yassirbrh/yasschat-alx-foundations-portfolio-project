from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .User import User
from .Message import Message
from .Friendship import Friendship
