from flask import Blueprint, request, jsonify
from init import db
from models.task import Task, tasks_schema, task_schema
from models.comment import Comment, comment_schema, comments_Schema
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required

tasks_bp = Blueprint('tasks', __name__, url_prefix='/task')

@tasks_bp.route('/')
def get_all_task():
    tasks = Task.query.all()
    result = tasks_schema.dump(tasks)
    return jsonify(result)

@tasks_bp.route('/<int:id>')
def get_one_task(id):
    stmt = db.select(Task).filter_by(id=id)
    task = db.session.scalar(stmt)
    if task:
        return task_schema.dump(task)
    else:
        return {'error': f'Task not found by id {id}'}, 404
    

@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    body_data = request.get_json()
    # Creat a new tasks instance
    task = Task(
        title=body_data.get('title'),
        description=body_data.get('description'),
        due_date=body_data.get('due_date'),
        created_at=body_data.get('created_at'),
        user_id=get_jwt_identity()
    )
    # add task to the session
    db.session.add(task)
    # commit the task
    db.session.commit()

    return task_schema.dump(task), 201

@tasks_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_task(id):
    try:
        task = Task.query.get(id)
        db.session.delete(task)
        db.session.commit()
        return {'message': f'Task {task.title} deleted successfully'}
    except:
        return {'error': f'Task not found with id {id}'}, 404

@tasks_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_task(id):
    # Fetches task with given id from database
    task = Task.query.get(id)
    # If the task is not found returns and error message
    if not task:
        return {'error': f'Task not found with id {id}'}, 404
    # Gets the data of json from the request
    data = request.get_json()
    #update the task attribute with new values
    for key, value in data.items():
        setattr(task, key, value)
        # Commit the changes and return a success message
    db.session.commit()
    return {'message': f'Task {task.title} Updated Successfully'}


# /task/task_id/comments

# API endpoint from comment ['POST']
@tasks_bp.route('/<int:task_id>/comments', methods=['POST'])
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
@tasks_bp.route('/<int:task_id>/comments/<int:comment_id>', methods=['DELETE'])

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

@tasks_bp.route('/<int:task_id>/comments/<int:comment_id>', methods=['PUT', 'PATCH'])
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