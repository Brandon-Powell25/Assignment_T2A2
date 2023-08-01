# R1 Identification of the problem you are trying to solve by building this particular app.

This Project is for users who want to make tasks and store tasks, it can be used for individuals and organisations. It is intended for people who like to write down a bunch of tasks, so they can keep track of were they are up to.

The application allow users to create and retrieve task as well as let then know when they created it at and when there due date of the task is. Organizations that have alot of work can become disorganize and stressed with alot of tasks.

Individuals can struggle with keeping track of their tasks, especially when they have alot to do, which can lead to forgotten task or missed deadlines for jobs or every day task.

# R2 Why is it a problem that needs solving?

Modern day is a very fast-paced work environment, it is important to stay organized and on top of task. But with so many task to manage, it can be easy to become overwhelmed, which is where a task management system comes in.

Individuals or teams can use a tasks management system so they can have organization in their work load and be able to piroritize tasks to make sure no task is left behind or forgotten. With all tasks in a single place team or individuals can see what need to be done and when, which help remove stress load and to be able to mange their time.

One key benefit if a task system is to improve collaborations. which can help team stay on the same page and make sure everyone is working towards the same goal, it can improve productivity, and make teams and individuals woork more efficiently and effectivly. 

# R3 Why have you chosen this database system. What are the drawbacks compared to others?

For my API webserver project i have choosen postgreSQL database management system.

I choose this database system because, PostgreSQL supports both relational and non-relational tables and because it is compatible with Python, Flask, and other third-party softwares like SQLAlchemy, Marashmallow, and JWT that are used in my application, it follows the ACID compliance for the project.

PostgreSQL has an open source, meaning its free to use and has a long history, with large communitys that provides sample resources and documents. It's also got high level security measures, which support User authentications and authorizations and it's able to hash for a one-way encryption of passwords.

Some drawbacks of postgreSQL is it can be more complex to set up and maintain.
For very large-scale application that require high levels of scalabilty postgreSQL may not be the best choice. PostgreSQL

https://www.guru99.com/introduction-postgresql.html

# R4 Identify and discuss the key functionalities and benefits of an ORM

The models in my project are User, Task, Comment found in file /src/models folder, the relationship and data have been defined with SQLAlchemy(db.model)

**User model:**

A User must register with thier name, email and password and then they can login with that to access my API. Once logged in they can create a task read task and make comment on theirs or other peoples tasks.

```
class User(db.Model):
# Define the table name
__tablename__ = 'users'
      
    # Sets the primary key for user
    id = db.Column(db.Integer, primary_key=True)

    # Defines the columns of the users table
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
```

-  ```__tablename__ ```  = users, defines the column name and data type and constraints.

- id column is defined as an integer primary key which increment through every new creation of a new user..

- Name, email, password and is_admin is defined as a string() or boolean set, they have the nullable= clause.

- is_admin will revert to false if a user does not a authorised as admin.

- **Relationships:**
    - User:
       - one to many relationship with task
       - One to many relationship with comment
       - many to many relationship many users can leave many comment on a certain task

**Task model:**

task.py

```
class Task(db.Model):
    # define table name for db
    __tablename__ = 'tasks'
    # Set the primary key
    id = db.Column(db.Integer, primary_key=True)

    # Other attributes
    title = db.Column(db.String(50))
    description = db.Column(db.Text)
    due_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Set foreign key for user_id
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship with other models
    comments = db.relationship('Comment', back_populates='tasks', foreign_keys=[Comment.task_id])
    user = db.relationship('User', back_populates='tasks', lazy='joined')
```
- __Tablename__= task, defines the table name to be mapped in model

- id = db.Column(db.Integer, primary_key=True) creates a column with the title 'id' of an integer data type, will also auto increment with each new tasks.

- Title and description is established wth their data type character limit (string() or Text()

- due_date and created_at is defined with date due_date you write you due_date in (year, month, day) and created_at is defined and automated time from when you created the task.

- **Relationship**
     - one to many relationship with comment model
     - many to one relationship wiht User model

db.relationship function as argument like back_populates, foregin_keys and lazy.

**Comment model**

comment.py


https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping

https://www.baeldung.com/cs/object-relational-mapping

# R5 Document all endpoints for your API

Endpoint in my API project are in the following format:

**Route: "/"**
- Methods: 
- @decorator
- Functionality
- Local host URL
- Example expected response

**The Local Host URL that I used was localhost:8080/**

# **AUTH ENDPOINTS:**

![Auth routes](<docs/auth routes.jpg>)

**URL prefix "/auth"**

**Route: "/register"**

- Method: POST
- @auth_bp.route('/register', methods=['POST])
- Functionality: Creates a new user, is_admin will return True , if there not admin it will return False.
- Local host URL: localhost:8080/auth/register
- Examples of expected response (user without admin):

![User register](docs/Register_user.jpg)


**Route: "/login"**

- Method: POST
- @auth_bp.route('/login', methods=[POST])
- Functionality: Allow a user to login and recieve there token only require 'Name', 'email', and 'password'.
- Local host URL: Localhost:8080/auth/login
- Example of login and there response(without admin):

![Non-admin User login](docs/User_login.jpg)

- Example of admin login and it response:

![Admin login](<docs/Admin login.jpg>)

# **USERS ENDPOINTS**

![User routes](<docs/user routes.jpg>)

**URL prefix '/users'**

**Route: '/'**

- Method: GET
- @user_bp.route('/', methods-['GET])
- Functionality: Return a list of users and how many task they have
- Local host URL: localhost:8080/users
- Example of getting all users and the response

![Example of all user](docs/Get_users.jpg)

**Route: '/int:user_id'**

- Method: GET
- @user_bp('/<int:user_id>', methods=['GET])
- Functionality: Returns a single user with specified id given
- Local host URL: localhost:8080/users/int:user_id
- Example of single users with response:

![Single User](docs/Get_user.jpg)

**Route: '/int:user_id'**

- Method: DELETE
- @user_bp.route('/<int:user_id>', methods=[DELETE])
- Functionality: Deletes a user with specified id
- local host URL: localhost:8080/users/int:user_id
- Example of user being deleted and response:

![DELETE user](docs/Delete_user.jpg)

# **TASKS ENDPOINTS**

![Task routes](<docs/Tasks routes.jpg>)

**URL prefix: '/task'**

**Route: '/'**

- Method: GET
- @tasks_bp.route('/', methods=['GET'])
- Functionality: Gets all users in db
- local host URL: localhost:8080/task
- Example of getting all task and response:

Example 1:
![GET all Task 1](docs/Get_all_tasks.jpg)

Example 2:
![All task 2](docs/Get_all_task3.jpg)

Example 3:
![All task 3](docs/Get_all_task2.jpg)

**Route: '/<int:id>'**

- Methods: GET
- tasks_bp.route('/<int:id>', methods=['GET'])
- Functionality: Gets a single user with specified id given.
- local host URL: localhost:8080/task/tasks_id
- Example of getting single task and response;

**Task 1:**
![Task 1](docs/Get_task1.jpg)

**Task 2:**
![Alt text](docs/get_task2.jpg)

**Task 6:**
![Alt text](docs/Get_Task.jpg)

**Route '/**

- Method: POST
- @tasks_bp.route('/', methods=['POST])
- Functionality: Creates a task
- local host URL: localhost:8080/task
- @JWT token requried
- Example of creating a task and the response:

Example 1:
![Creating a task](docs/Create_task.jpg)

Example 2:
![Creating a task](docs/Create_task2.jpg)

**Route '/id'**

- Methods: DELETE
- task_bp.route('/<int:id>', methods=[DELETE])
- Functionality: Deletes a task with the specified id given
- local host URL: localhost8080/task/task_id
- @jwt_required
- Examples of deleting a task:

Example 1:
![Delete task 9](docs/Delete_task.jpg)

Example 2:
![Delete task 11](docs/Delete_task2.jpg)

**Route '/id'**

- Methods: PUT, PATCH
- Functionality: Updates a task
- local host URL: localhost:8080/task/task_id
- @jwt_required 'Token'
- Example of updating task and response:

Example 1:
![updating task](<docs/Update task.jpg>)

Example 2 when you look at all task again:
![Updated task](<docs/Updated task.jpg>)

# **COMMENT ROUTES**

![Comment routes in Postman](<docs/Comment routes.jpg>)

**URL prefix: '/tasks/int:task_id/comments**

**Route '/'**

- Method: POST
- Functionality: Creates a comment on a users task or their own
- localhost URL: localhost:8080/task/task_id/comments
- @jwt_required 'Token'
- Example of creating a comment:

Example:
![Alt text](docs/Create_comment.jpg)

**Route '/int:comment_id'**

- Methods: PUT, PATCH
- Functionality: Updating a comment
- localhost:8080/task/task_id/comments/comment_id
- @jwt_required 'Token'
- Example of updating comment:

![Alt text](docs/Updating_comment.jpg)

**Route: '/int:comment_id'**

- Method: DELETE
- Functionality: Deleteing a comment
- local hosat URL: localhost:8080/tasks/tasks_id/comments/comment_id
- @jwt_required 'Token'
- Example of deleting comment:

![Delete task 1](docs/Deleteing_comment.jpg)

# R6 An ERD for your app

![ERD](docs/ERD.jpg)

# R7 Detail any third party services that your app will use

**Postman** was used to test my API endpoints functiionality

![Alt text](docs/Postman.jpg)

# R8 Describe your projects models in terms of the relationships they have with each other

# R9 Discuss the database relations to be implemented in your application

# R10 Describe the way tasks are allocated and tracked in your project















https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.DateTime.python_type
https://stackoverflow.com/questions/48592639/updating-a-record-with-wtforms-sqlalchemy-flask
https://stackoverflow.com/questions/6699360/flask-sqlalchemy-update-a-rows-information