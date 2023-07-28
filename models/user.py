from init import db, ma
from datetime import datetime
from marshmallow import fields
from models.task import Task
from models.comment import Comment

class User(db.Model):
    # Define the table name
    __tablename__ = 'users'

    # Defines the columns of the users table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

    tasks = db.relationship('Task', back_populates='user', cascade='all, delete')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    tasks = fields.List(fields.Nested('TaskSchema', exclude=['user']))
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'created_at', 'is_admin', 'tasks')

user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(many=True, exclude=['password'])