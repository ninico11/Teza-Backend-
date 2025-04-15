import os
import tempfile
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from ..tools.audio_trans import transcribe_audio  # Adjust the import according to your project structure

audio = Blueprint('audio', __name__)

@audio.route('/voice_to_text', methods=['POST'])
def voice_to_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    filename = secure_filename(file.filename)
    
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, filename)
    
    file.save(temp_path)

    try:
        audio = open(temp_path, 'rb')
        transcription_text = transcribe_audio(audio)
        audio.close()
    except Exception as e:
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return jsonify({"text": transcription_text}), 201
