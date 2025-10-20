from app import socketio
from flask_socketio import emit

# This handles the 'connect' event from a new client
@socketio.on('connect')
def handle_connect():
    print('Client connected!')
    emit('server_message', {'data': 'Welcome to the WebSocket demo!'})

# This handles the 'client_message' event sent from the HTML page
@socketio.on('client_message')
def handle_client_message(message):
    print('Received message: ' + message['data'])
    # Echo the message back to ALL connected clients (broadcast=True)
    emit('server_message', {'data': '<b>User:</b> ' + message['data']}, broadcast=True)

# This handles the built-in 'disconnect' event
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')