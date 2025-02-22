from flask import Flask
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')

def create_app():
    app = Flask(__name__)
    # Application configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", None)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", 'supersecretkey')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    
    # Enable token blacklist support
    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access"]

    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)

    # Register blueprints
    from .apis.auth import auth
    from .apis.communication import communication
    app.register_blueprint(auth)
    app.register_blueprint(communication)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        
    return app
