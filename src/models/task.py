from init import db, ma 
from datetime import datetime
from marshmallow import fields
from models.comment import Comment
from marshmallow.validate import Length, And, Regexp

class Task(db.Model):
    # define table name for db
    __tablename__ = 'tasks'
    # Set the primary key
    id = db.Column(db.Integer, primary_key=True)

    # Other attributes
    title = db.Column(db.String(50))
    description = db.Column(db.Text)
    due_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Set foreign key for user_id
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship with other models
    comments = db.relationship('Comment', back_populates='tasks', foreign_keys=[Comment.task_id])
    user = db.relationship('User', back_populates='tasks', lazy='joined')

class TaskSchema(ma.Schema):    
    user = fields.Nested('UserSchema', only=['name', 'email'])
    comments = fields.List(fields.Nested('CommentSchema'), exclude=['task'])

    title = fields.String(required=True, validate=And(
        Length(min=2, error='Title must be 2 characters or more'),
        Regexp('^[a-zA-z0-9 ]+$', error='Can only be letters numbers and spaces')
    ))

    class Meta:
        fields = ('id', 'title', 'description', 'due_date', 'created_at', 'updated_at', 'user', 'comments')
        ordered = True

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)