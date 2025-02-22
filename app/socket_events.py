from app import socketio
from flask_socketio import join_room

@socketio.on('join')
def handle_join(data):
    """
    Expect data like: { "room": "conversation_1_2" }
    """
    room = data.get("room")
    if room:
        join_room(room)
        print(f"Joined room: {room}")  # For server-side debugging
        socketio.emit('join_response', {'msg': f'Joined {room}'}, to=room)
