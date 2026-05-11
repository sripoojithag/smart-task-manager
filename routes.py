from flask import (
    request,
    jsonify,
    render_template,
    redirect,
    url_for
)

from app import app, db, socketio

from datetime import datetime

from models import Task, User

from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# ======================================
# REGISTER
# ======================================
@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:

        return redirect(
            url_for('home')
        )

    if request.method == 'POST':

        username = request.form.get(
            'username'
        ).strip()

        password = request.form.get(
            'password'
        )

        if not username or not password:

            return render_template(
                'register.html',
                error='All fields are required'
            )

        if len(password) < 4:

            return render_template(
                'register.html',
                error='Password too short'
            )

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:

            return render_template(
                'register.html',
                error='Username already exists'
            )

        hashed_password = generate_password_hash(
            password
        )

        new_user = User(
            username=username,
            password=hashed_password
        )

        db.session.add(new_user)

        db.session.commit()

        # AUTO LOGIN AFTER REGISTER

        login_user(new_user)

        return redirect(
            url_for('home')
        )

    return render_template(
        'register.html',
        error=None
    )

# ======================================
# LOGIN
# ======================================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect(url_for('home'))

        return render_template(
            'login.html',
            error='Invalid Credentials'
        )

    return render_template('login.html',error=None)

# ======================================
# LOGOUT
# ======================================

@app.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for('login'))

# ======================================
# GET TASKS
# ======================================

@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():

    tasks = Task.query.filter_by(
        user_id=current_user.id
    ).all()

    return jsonify([

        {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'status': task.status,
            'deadline': str(task.deadline) if task.deadline else ''
        }

        for task in tasks

    ])

# ======================================
# ADD TASK
# ======================================

@app.route('/api/tasks', methods=['POST'])
@login_required
def add_task():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                'error': 'No data received'
            }), 400

        title = data.get('title')

        if not title:

            return jsonify({
                'error': 'Title is required'
            }), 400

        # SAFE DATE
        deadline_value = None

        if (
            data.get('deadline')
            and data.get('deadline').strip()
        ):

            deadline_value = datetime.strptime(
                data.get('deadline'),
                '%Y-%m-%d'
            ).date()

        new_task = Task(

            title=title,

            description=data.get(
                'description',
                ''
            ),

            priority=data.get(
                'priority',
                'Medium'
            ),

            deadline=deadline_value,

            status='Pending',

            user_id=current_user.id
        )

        db.session.add(new_task)

        db.session.commit()

        socketio.emit(
            'task_update',
            {
                'message': 'Task Added'
            }
        )

        return jsonify({
            'message': 'Task created successfully'
        }), 201

    except Exception as e:

        print("BACKEND ERROR:", str(e))

        db.session.rollback()

        return jsonify({
            'error': str(e)
        }), 500

# ======================================
# UPDATE TASK
# ======================================

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):

    try:

        task = Task.query.filter_by(
            id=task_id,
            user_id=current_user.id
        ).first()

        if not task:

            return jsonify({
                'error': 'Task not found'
            }), 404

        data = request.get_json()

        task.title = data.get(
            'title',
            task.title
        )

        task.description = data.get(
            'description',
            task.description
        )

        task.priority = data.get(
            'priority',
            task.priority
        )

        if (
            data.get('deadline')
            and data.get('deadline').strip()
        ):

            task.deadline = datetime.strptime(
                data.get('deadline'),
                '%Y-%m-%d'
            ).date()

        task.status = data.get(
            'status',
            task.status
        )

        db.session.commit()

        socketio.emit(
            'task_update',
            {
                'message': 'Task Updated'
            }
        )

        return jsonify({
            'message': 'Task updated successfully'
        })

    except Exception as e:

        print("UPDATE ERROR:", str(e))

        db.session.rollback()

        return jsonify({
            'error': str(e)
        }), 500

# ======================================
# DELETE TASK
# ======================================

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):

    try:

        task = Task.query.filter_by(
            id=task_id,
            user_id=current_user.id
        ).first()

        if not task:

            return jsonify({
                'error': 'Task not found'
            }), 404

        db.session.delete(task)

        db.session.commit()

        socketio.emit(
            'task_update',
            {
                'message': 'Task Deleted'
            }
        )

        return jsonify({
            'message': 'Task deleted successfully'
        })

    except Exception as e:

        print("DELETE ERROR:", str(e))

        db.session.rollback()

        return jsonify({
            'error': str(e)
        }), 500