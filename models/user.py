from init import db, ma
from datetime import datetime

class User(db.model):
    # Defines the columns of the users table
    id = db.column(db.Integer, primary_key=True)
    name = db.colum(db.string(50))
    email = db.colum(db.string(100), nullable=False, unique=True)
    password = db.column(db.string(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserSchema(ma.schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'created_at')

user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])