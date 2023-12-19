from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'User'
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(255), unique=True, nullable=False)
    FullName = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Created_At = db.Column(db.DateTime, default=datetime.utcnow)
    Last_Active = db.Column(db.DateTime, default=datetime.utcnow)
