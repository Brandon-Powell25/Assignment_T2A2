from flask import Blueprint, request
from init import db
from models.task import Task
from models.comment import Comment , comment_schema, comments_Schema
from flask_jwt_extended import jwt_required, get_jwt_identity

comments_bp = Blueprint('comments', __name__, url_prefix='/<int:task_id>/comments')

# /task/task_id/comments

# API endpoint from comment ['POST']
@comments_bp.route('/', methods=['POST'])
# JWT token required
@jwt_required()
def create_comment(task_id):
    # Fetches the data from json
    body_data = request.get_json()
    task = Task.query.get(task_id)
    if task:
        comment = Comment(
            comment=body_data.get('comment'),
            user_id=get_jwt_identity(),
            tasks=task
        )
        db.session.add(comment)
        db.session.commit()
        return comment_schema.dump(comment), 201
    else:
        return {'error': f'Task not found with id {task_id}'}, 404
    
# API Endpoint for deleteing comments
@comments_bp.route('/<int:comment_id>', methods=['DELETE'])

# JWT token required
@jwt_required()
def delete_comment(task_id, comment_id):
    # Get the task wiht the give task_id
    task = Task.query.get(task_id)
    # Check if task exists
    if task:
        # Fetchs the comment with the given comment_id associated with the task
        comment = Comment.query.filter_by(id=comment_id, task_id=task.id).first()
        # Check if comments exists
        if comment:
            # Delete the comment and commit it from the database
            db.session.delete(comment)
            db.session.commit()
            # Return a succes message
            return {'message': f'Comment with id {comment.id} deleted'}, 200
        else:
            # return error message if comment not found
            return {'error': f'comment not found with id {comment_id}'}, 404
    else:
        # Return a error message if task not found
        return {'error': f'Task not found wiht id {task_id}'}, 404

@comments_bp.route('/<int:comment_id>', methods=['PUT', 'PATCH'])
@jwt_required
def update_comment(task_id, comment_id):
    # Retrieve the task with giving id
    task = Task.query.get(task_id)
    # Check if task exist
    if not task:
        return {'error': f'Task not fount with id {task_id}.'}, 404
    
    # Retrieves the comment wiht the given comment_id associated with the task
    comment = Comment.query.filter_by(id=comment_id, task_id=task.id).first()

    # Check if comment exists
    if not comment:
        return {'error': f'Comment not found with id {comment_id}.'}, 404
    
    # Gets the request data from json
    data = request.get_json()

    # Update the comment content with the new data
    if 'content' in data:
        comment.content = data['content']

    # Commit the changes to the database
    db.session.commit()

    # Return a success message
    return {'message': f'Comment with id {comment.id} has been updated.'}, 200 