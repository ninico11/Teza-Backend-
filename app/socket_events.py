from app import socketio
from flask_socketio import join_room

@socketio.on('join')
def handle_join(data):
    room = data.get("room")
    if room:
        join_room(room)
        print(f"Joined room: {room}")
        socketio.emit('join_response', {'msg': f'Joined {room}'}, room=room)

@socketio.on('connect')
def handle_connect():
    """Handle new WebSocket connection."""
    socketio.emit('connected', {'message': 'WebSocket connected successfully'})
