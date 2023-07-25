from init import db, ma 
from datetime import datetime
from marshmallow import fields

# association table
task_comments = db.Table('task_comments',
                         db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
                         db.Column('comment_id', db.Integer, db.ForeignKey('comment.id'), primary_key=True)
                        )

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', back_populates='tasks')

    comments = db.relationship('Comment', secondary=task_comments, back_populates='tasks')

class TaskSchema(ma.Schema):    
    user = fields.Nested('UserSchema', only=['name', 'email'])
    comments = fields.List(fields.Nested('commentSchema'), exclude=['task'])
    
    class Meta:
        fields = ('id', 'title', 'description', 'due_date', 'created_at', 'updated_at', 'user')
        ordered = True

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)