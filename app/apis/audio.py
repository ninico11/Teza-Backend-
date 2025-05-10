import os
import tempfile
import json
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from ..tools.audio_trans import transcribe_audio
from ..tools.translation import translate_message_event
audio = Blueprint('audio', __name__)

@audio.route('/voice_to_text', methods=['POST'])
def voice_to_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided."}), 400

    file = request.files['file']
    requested_language = request.form.get('requested_language', 'en')

    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    filename = secure_filename(file.filename)
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, filename)
    file.save(temp_path)

    try:
        with open(temp_path, 'rb') as audio_file:
            print(str(audio_file))
            content = transcribe_audio(audio_file)
            translated_text = translate_message_event(content, requested_language)
            if not isinstance(translated_text, dict):
                translated_text = json.loads(translated_text)
    except Exception as e:
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return jsonify({"translated_text": translated_text["translated_message"], "original": content}), 201
