from init import db, ma
from task import task_comments
from marshmallow import fields

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', back_populates='comments')
    tasks = db. relationship('Task', secondary=task_comments, back_populate='comments')

class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    task = fields.Nested('TaskSchema', exclude=['comments'])

    class meta:
        fields = ('id', 'comment', 'task', 'user')
        ordered = True

commment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)