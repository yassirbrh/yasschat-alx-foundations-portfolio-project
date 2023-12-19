from . import db
from datetime import datetime

class Friendship(db.Model):
    __tablename__ = 'Friendship'

    FriendshipID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    FriendID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    isAccepted = db.Column(db.Boolean, nullable=False)

    # Establishing the relationship with the User model
    user = db.relationship('User', foreign_keys=[UserID])
    friend = db.relationship('User', foreign_keys=[FriendID])

    def __init__(self, user_id, friend_id, is_accepted):
        self.UserID = user_id
        self.FriendID = friend_id
        self.isAccepted = is_accepted
