from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, User, Message, MessageTranslation
from ..tools.translation import translate_message
from .. import socketio

communication = Blueprint('communication', __name__)

@communication.route('/messages', methods=['POST'])
@jwt_required()
def send_message():
    """
    Send a message from the authenticated user to another user.
    Expected JSON body:
    {
        "receiver_id": <int>,
        "content": "Your message text",
        "language_code": "en",         # The language of the original message
        "requested_language": "es"       # The language to translate the message into
    }
    """
    data = request.get_json()
    sender_id = get_jwt_identity()
    receiver_id = data.get('receiver_id')
    content = data.get('content')
    language_code = data.get('language_code')
    requested_language = data.get('requested_language')

    # Validate required fields
    if not all([receiver_id, content, language_code, requested_language]):
        return jsonify({'msg': 'receiver_id, content, language_code, and requested_language are required.'}), 400

    # Check if receiver exists
    receiver = User.query.get(receiver_id)
    if not receiver:
        return jsonify({'msg': 'Receiver not found.'}), 404

    # Create the original message record
    message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
        language_code=language_code
    )
    db.session.add(message)
    db.session.commit()  # Commit to obtain message.id

    # Translate the message using the provided translation function
    translated_text = translate_message(content, requested_language)

    # Create a translation record linked to the message
    translation = MessageTranslation(
        message_id=message.id,
        target_language=requested_language,
        translated_text=translated_text
    )
    db.session.add(translation)
    db.session.commit()

    # Build conversation room name (both clients should join the same room)
    room = f"conversation_{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}"
    message_data = {
        'id': message.id,
        'sender_id': message.sender_id,
        'receiver_id': message.receiver_id,
        'content': message.content,
        'language_code': message.language_code,
        'created_at': message.created_at.isoformat() if message.created_at else None,
        'translation': {
            'id': translation.id,
            'target_language': translation.target_language,
            'translated_text': translation.translated_text,
            'translated_at': translation.translated_at.isoformat() if translation.translated_at else None
        }
    }
    # Emit the new message to the room so connected clients can update in real time
    socketio.emit('new_message', message_data, room=room)

    return jsonify({
        'msg': 'Message sent successfully.',
        'message': {
            'id': message.id,
            'sender_id': message.sender_id,
            'receiver_id': message.receiver_id,
            'content': message.content,
            'language_code': message.language_code,
            'created_at': message.created_at
        },
        'translation': {
            'id': translation.id,
            'target_language': translation.target_language,
            'translated_text': translation.translated_text,
            'translated_at': translation.translated_at
        }
    }), 201

@communication.route('/messages/<int:other_user_id>', methods=['GET'])
@jwt_required()
def get_conversation(other_user_id):
    """
    Retrieve all messages exchanged between the authenticated user and another user.
    This returns both the original message and any translations.
    """
    current_user_id = get_jwt_identity()
    
    # Fetch messages where the authenticated user is either sender or receiver
    messages = Message.query.filter(
        ((Message.sender_id == current_user_id) & (Message.receiver_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.receiver_id == current_user_id))
    ).order_by(Message.created_at).all()

    if not messages:
        return jsonify({'msg': 'No conversation found.'}), 404

    conversation = []
    for msg in messages:
        # For each message, include all translations (if any)
        translations = [{
            'id': t.id,
            'target_language': t.target_language,
            'translated_text': t.translated_text,
            'translated_at': t.translated_at
        } for t in msg.translations]

        conversation.append({
            'id': msg.id,
            'sender_id': msg.sender_id,
            'receiver_id': msg.receiver_id,
            'content': msg.content,
            'language_code': msg.language_code,
            'created_at': msg.created_at,
            'translations': translations
        })

    return jsonify({'conversation': conversation}), 200
