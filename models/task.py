from init import db, ma 
from datetime import datetime
from marshmallow import fields

class task(db.Model):
    __tablename__ = 'Tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1000))
    due_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.datetime, default=datetime.utcnow)
    updated_at = db.Column(db.Datetime, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = db.relationship('User', secondary='User_task', backref='tasks')

class TaskSchema(ma.Schema):
    
    user = fields.nested('UserSchema', only=['name, email'])
    
    class Meta:
        fields = ('id', 'title', 'description', 'due_date', 'created_at', 'updated_at', 'user')
        ordered = True

task_schema = TaskSchema()
tasks_schema = (many=True)