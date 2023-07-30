from init import db, ma
from marshmallow import fields

class Comment(db.Model):
    # Table name
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)

    user = db.relationship('User', back_populates='comments')
    tasks = db.relationship('Task', back_populates='comments')

class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    tasks = fields.Nested('TaskSchema', exclude=['comments'])

    class Meta:
        fields = ('id', 'comment', 'tasks', 'user')
        ordered = True

comment_schema = CommentSchema()
comments_Schema = CommentSchema(many=True)
