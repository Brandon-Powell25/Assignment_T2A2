from flask import Blueprint, request, jsonify
from init import db
from models.task import Task, tasks_schema, task_schema
from models.comment import Comment, comment_schema, comments_Schema
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required
from controllers.comment_controller import comments_bp

tasks_bp = Blueprint('tasks', __name__, url_prefix='/task')
tasks_bp.register_blueprint(comments_bp)

@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_task():
    tasks = Task.query.all()
    result = tasks_schema.dump(tasks)
    return jsonify(result)

@tasks_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
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
    body_data = task_schema.load(request.get_json())
    # Creat a new tasks instance
    task = Task(
        title=body_data.get('title'),
        description=body_data.get('description'),
        due_date=body_data.get('due_date'),
        created_at=body_data.get('created_at'), # Month, date, Year 
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
@jwt_required()
def update_task(id):
    # Fetches task with given id from database
    task = Task.query.get(id)
    # If the task is not found returns and error message
    if not task:
        return {'error': f'Task not found with id {id}'}, 404
    # Gets the data of json from the request
    data = task_schema.load(request.get_json(), partial=True)
    #update the task attribute with new values
    for key, value in data.items():
        setattr(task, key, value)
        # Commit the changes and return a success message
    db.session.commit()
    return {'message': f'Task {task.title} Updated Successfully'}


