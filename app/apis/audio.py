import os, tempfile, json
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from ..tools.audio_trans import transcribe_audio
from ..tools.translation import translate_message_event
audio = Blueprint("audio", __name__)

@audio.route("/voice_to_text", methods=["POST"])
def voice_to_text():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    upload = request.files["file"]
    if upload.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save exactly as-is in /tmp
    tmp_dir  = tempfile.gettempdir()
    src_path = os.path.join(tmp_dir, secure_filename(upload.filename))
    upload.save(src_path)

    try:
        with open(src_path, "rb") as fh:
            transcript = transcribe_audio(fh)          # <-- raw file, no conversion

        requested_language = request.form.get("requested_language", "en")
        translated = translate_message_event(transcript, requested_language)
        if not isinstance(translated, dict):
            translated = json.loads(translated)

    except Exception as exc:
        return jsonify({"error": f"Transcription failed: {exc}"}), 500
    finally:
        if os.path.exists(src_path):
            os.remove(src_path)

    return (
        jsonify(
            {
                "translated_text": translated["translated_message"],
                "original": transcript,
            }
        ),
        201,
    )
