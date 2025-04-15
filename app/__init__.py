from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from .apis.communication import communication
    from .apis.audio import audio
    app.register_blueprint(communication)
    app.register_blueprint(audio)
        
    return app
