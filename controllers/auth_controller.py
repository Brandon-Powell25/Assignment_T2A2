from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, user_schema, users_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def auth_register():
    try:
        body_data = request.get_json()

        user = User()
        user.name = body_data.get('name')
        user.email = body_data.get('email')
        user.password = bcrypt.generate_password_hash(body_data.get('password')).decode('utf-8')

        # adds the users to the session
        db.session.add(user)
        # commit to add the user to database
        db.session.commit()
        # respond to the client
        return user_schema.dump(user), 201
        
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return { 'errorr': 'Email address already in use'}, 409
        if err.orig.pgcode == errorcodes.NOT_VULL_VIOLATION:
            return { 'error': 'Email is required'}
        