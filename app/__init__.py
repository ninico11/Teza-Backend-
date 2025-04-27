from flask import Flask
from flask_cors import CORS        

def create_app():
    app = Flask(__name__)

    CORS(app)                        

    # blueprints
    from .apis.communication import communication
    from .apis.audio import audio
    from .apis.sentiment import sentiment
    app.register_blueprint(communication)
    app.register_blueprint(audio)
    app.register_blueprint(sentiment)

    return app
