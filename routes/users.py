from flask import Blueprint, jsonify, request
from models import db, User
from schemas import serialize_user

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/users', methods=['POST'])
def create_or_get_user():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('zone'):
        return jsonify({"error": "Los campos username y zone son obligatorios"}), 400

    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify(serialize_user(existing_user)), 200

    new_user = User(
        username=data['username'],
        zone=data['zone'],
        email=data.get('email')
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(serialize_user(new_user)), 201