from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt, get_jwt_identity
)
from ..models import db, User
from .. import jwt

auth = Blueprint('auth', __name__)

blacklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in blacklist

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Extract required fields
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')  # Optional field

    if not username or not email or not password:
        return jsonify({'msg': 'Username, email, and password are required.'}), 400

    # Check if the email is already registered
    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'A user with that email already exists.'}), 400

    # Hash the password for secure storage
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password, phone=phone)

    db.session.add(new_user)
    db.session.commit()

    # Convert user.id to string when creating the token
    access_token = create_access_token(identity=str(new_user.id))
    return jsonify({'msg': 'User created successfully.', 'access_token': access_token}), 201

@auth.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'msg': 'Email and password are required.'}), 400

    user = User.query.filter_by(email=email).first()

    # Verify user exists and the password is correct
    if not user or not check_password_hash(user.password, password):
        return jsonify({'msg': 'Invalid email or password.'}), 401

    # Convert user.id to string when creating the token
    access_token = create_access_token(identity=str(user.id))
    return jsonify({'msg': 'Logged in successfully.', 'access_token': access_token}), 200

@auth.route('/signout', methods=['POST'])
@jwt_required()
def signout():
    # Revoke the current token by adding its jti to the blacklist
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify({'msg': 'Successfully logged out. Token revoked.'}), 200
