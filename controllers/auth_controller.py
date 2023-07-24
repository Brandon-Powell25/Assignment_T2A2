from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, user_schema, users_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta

# Creates a Flask Blueprint with the /auth endpoint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# POST endpoint to register a user
@auth_bp.route('/register', methods=['POST'])
def auth_register():
    # try block
    try:
        body_data = request.get_json()
        # Creates a new user instance from the user info
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
    # except error block    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            error_message = 'Email address already in use'
        elif err.orig.pgcode == errorcodes.NOT_VULL_VIOLATION:
            error_message = f'The {err.orig.diag.column_name} is required'
        return { 'error': error_message}
        

@auth_bp.route('/login', methods=['POST'])
def auth_login():
    body_data = request.get_json()
    # find the user by their email
    stmt = db.select(User).filter_by(email=body_data.get('email'))
    user = db.session.scalar(stmt)
    # if user exist and password is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get('password')):
        token = create_access_token(identity=str(user.id), expires_delta=False)
        return { 'email': user.email, 'token': token, 'is_admin': user.is_admin}
    else:
        return { 'error': 'Invalid email or password'}, 401
   