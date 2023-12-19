#!/usr/bin/python3
'''
    This is the entry point of the application
'''
from app import app, socketio


if __name__ == "__main__":
    socketio.run(app, port=5000)
