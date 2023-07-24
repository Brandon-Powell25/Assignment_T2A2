from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.task import Task
from datetime import datetime

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_all():
    db.create_all()
    print("Tables Created")

@db_commands.cli.command('drop')
def drop_all():
    db.drop_all()
    print('Tables Dropped')

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            name='Brandon',
            email='Brandon@admin.com',
            password=bcrypt.generate_password_hash('12345').decode('utf-8'),
            is_admin=True
        ),
        User(
        name = 'Jeffery',
        email = 'jeffery@email.com',
        password=bcrypt.generate_password_hash('Jeff12').decode('utf-8')
        )
    ]

    db.session.add_all(users)

    tasks = [
        Task(
            title='House Chores',
            description='Clean kitchen and mop',
            created_at=datetime.now(),
            due_date=datetime(2023, 7, 23 ),
            updated_at=datetime.now(),
            user=users[0]
        ),
        Task(
            title='House chores',
            description='Mow the lawn',
            created_at=datetime.now(),
            due_date=datetime(2023, 7, 26),
            updated_at=datetime.now(),
            user=users[0]
        ),
        Task(
            title='Training',
            description='2 x 20 push-ups, 2 x 20 sit-ups, 2 x 20 body weight squats every Monday, Wednesday, and Friday',
            created_at=datetime.now(),
            due_date=datetime(2030, 7, 30),
            user=users[0]
        ),
        Task(
            title='Training',
            description='2 x 20 bench press at 25kg, 2 x 20 row at 20kg, 2 x deadlift at 35kg',
            created_at=datetime.now(),
            due_date=datetime(2030, 7, 30),
            user=users[0]
        ),
        Task(
            title='Complete assignment',
            description='Complete my API webserver project',
            created_at=datetime.now(),
            due_date=datetime(2023, 7, 30),
            user=users[1]
        )
    ]
    db.session.add_all(tasks)

    # commits all tasks
    db.session.commit()

    print('Tables Seeded')