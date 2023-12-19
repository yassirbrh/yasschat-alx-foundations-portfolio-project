from . import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = 'Message'

    MessageID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SenderID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    ReceiverID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    Message = db.Column(db.String(255), nullable=False)
    Timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    isRead = db.Column(db.Boolean, default=False, nullable=False)

    # Define relationships
    sender = db.relationship('User', foreign_keys=[SenderID], backref=db.backref('sent_messages', lazy='dynamic'))
    receiver = db.relationship('User', foreign_keys=[ReceiverID], backref=db.backref('received_messages', lazy='dynamic'))
