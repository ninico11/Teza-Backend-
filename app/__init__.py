from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from .apis.communication import communication
    app.register_blueprint(communication)
        
    return app
