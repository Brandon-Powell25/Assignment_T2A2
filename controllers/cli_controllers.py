from flask import Blueprint
from init import db, bcrypt
from models.user import User

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_db()
    print("Tables Created")

@db_commands.cli.command('drop')
def drop_db():
    db.drop_db()
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
    db.session.commit()

    print('Tables Seeded')