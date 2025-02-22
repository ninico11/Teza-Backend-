from app import create_app
from app import socketio
import os

app = create_app()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)

