from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.task import Task
from models.comment import Comment
from datetime import date

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
            created_at=date(2023, 7, 22),
            due_date=date(2023, 7, 23 ),
            user=users[0]
        ),
        Task(
            title='House chores',
            description='Mow the lawn',
            created_at=date(2023, 7, 25),
            due_date=date(2023, 7, 26),
            user=users[0]
        ),
        Task(
            title='Training',
            description='2 x 20 push-ups, 2 x 20 sit-ups, 2 x 20 body weight squats every Monday, Wednesday, and Friday',
            created_at=date(2023, 7, 20),
            due_date=date(2030, 7, 30),
            user=users[0]
        ),
        Task(
            title='Training',
            description='2 x 20 bench press at 25kg, 2 x 20 row at 20kg, 2 x deadlift at 35kg',
            created_at=date(2023, 7, 20),
            due_date=date(2030, 7, 30),
            user=users[0]
        ),
        Task(
            title='Complete assignment',
            description='Complete my API webserver project',
            created_at=date(2023, 7, 18),
            due_date=date(2023, 7, 30),
            user=users[0]
        ),
        Task(
            title='Complete Diagram',
            description='Complete my ERD diagram',
            created_at=date(2023, 7, 20),
            due_date=date(2023, 7, 20),
            user=users[0]
        ),
        Task(
            title='Application',
            description='Do intial setup',
            created_at=date(2023, 7, 21),
            due_date=date(2023, 7, 21),
            user=users[0]
        ),
        Task(
            title='Application',
            description='Do Models files',
            created_at=date(2023, 7, 22),
            due_date=date(2023, 7, 24),
            user=users[0]
        )
    ]
    db.session.add_all(tasks)

    comments = [
        Comment(
            comment="Need to get on top of cleaning",
            user=users[0],
            tasks=tasks[0]
        ),
        Comment(
            comment='What a good work-out',
            user=users[0],
            tasks=tasks[2]
        ),
        Comment(
            comment="Where do you train?",
            user=users[1],
            tasks=tasks[2]
        ),
        Comment(
            comment="I train at home",
            user=users[0],
            tasks=tasks[2]
        ),
        Comment(
            comment='ERD was fun to try get right',
            user=users[0],
            tasks=tasks[5]
        ),
        Comment(
            comment='is it clean to mums expectation',
            user=users[1],
            tasks=tasks[0]
        )
    ]
    db.session.add_all(comments)
    # commits all tasks
    db.session.commit()

    print('Tables Seeded')