import eventlet
eventlet.monkey_patch()

from app import app, socketio

# This is what Gunicorn will call
application = socketio
