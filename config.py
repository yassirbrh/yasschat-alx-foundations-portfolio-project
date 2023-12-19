#!/usr/bin/python3
import secrets

class Config:
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Yassir2001@localhost:3306/YassChat'
    REDIS_URL = 'redis://localhost'
