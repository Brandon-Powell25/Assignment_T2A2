from flask import Blueprint, request, jsonify
from init import db
from models.task import Task, tasks_schema, task_schema

task_bp = Blueprint('tasks', __name__, url_prefix='/task')

@task_bp.route('/')
def get_all_task():
    tasks = Task.query.all()
    result = tasks_schema.dump(tasks)
    return jsonify(result)