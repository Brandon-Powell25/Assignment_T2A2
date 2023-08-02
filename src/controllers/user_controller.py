from flask import Blueprint, jsonify, request
from models.user import User, user_schema, users_schema
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity

# Set the blueprint with a url prefix /users
user_bp = Blueprint('user', __name__, url_prefix='/users')

# GET method for all users in db
@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()
    result = users_schema.dump(users)
    return jsonify(result), 200

# GET method to get a single user
@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    #check if user exist
    if not user:
        return jsonify({'message': 'User not with found with that id'}), 404
    result = user_schema.dump(user)
    return jsonify(result), 200

# DELETE method for users
@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    # Check if user exist if not will return a error message
    if not user:
        return jsonify({'error': 'user not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfullly'}), 200
