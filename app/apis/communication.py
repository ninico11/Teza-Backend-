from flask import Blueprint, request, jsonify
import json
from ..tools.translation import translate_message_event

communication = Blueprint('communication', __name__)

@communication.route('/translate_message', methods=['POST'])
def translate_message():
    data = request.get_json()
    content = data.get('message')
    requested_language = data.get('requested_language')

    # Translate the message using the provided translation function
    translated_text = translate_message_event(content, requested_language)
    if not isinstance(translated_text, dict):
                translated_text = json.loads(translated_text)
    
    return jsonify({
        'translatedText': translated_text["translated_message"],
    }), 201