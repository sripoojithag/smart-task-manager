from flask import Flask, render_template, jsonify
from flask_login import (
    LoginManager,
    login_required,
    current_user
)
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np

from models import db, User, Task

# ======================================
# LOAD ENV VARIABLES
# ======================================
load_dotenv()

# ======================================
# CREATE FLASK APP
# ======================================
app = Flask(__name__)

# ======================================
# APP CONFIGURATION
# ======================================
app.config['SECRET_KEY'] = os.getenv(
    'SECRET_KEY',
    'internship_task_secret'
)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ======================================
# INITIALIZE DATABASE
# ======================================
db.init_app(app)

# ======================================
# INITIALIZE SOCKETIO
# ======================================
socketio = SocketIO(
    app,
    cors_allowed_origins="*"
)

# ======================================
# LOGIN MANAGER
# ======================================
login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'

# ======================================
# USER LOADER
# ======================================
@login_manager.user_loader
def load_user(user_id):

    return db.session.get(
        User,
        int(user_id)
    )

# ======================================
# HOME PAGE
# ======================================
@app.route('/')
@login_required
def home():

    return render_template('index.html')

# ======================================
# ANALYTICS API
# ======================================
@app.route('/api/analytics')
@login_required
def get_analytics():

    tasks = Task.query.filter_by(
        user_id=current_user.id
    ).all()

    if not tasks:

        return jsonify({
            'total': 0,
            'completed': 0,
            'pending': 0,
            'percentage': 0
        })

    # CREATE DATAFRAME
    df = pd.DataFrame([
        {
            'status': task.status
        }
        for task in tasks
    ])

    total_tasks = len(df)

    completed_tasks = len(
        df[df['status'] == 'Completed']
    )

    pending_tasks = (
        total_tasks - completed_tasks
    )

    completion_percentage = np.round(
        (completed_tasks / total_tasks) * 100,
        2
    )

    return jsonify({
        'total': total_tasks,
        'completed': completed_tasks,
        'pending': pending_tasks,
        'percentage': float(
            completion_percentage
        )
    })

# ======================================
# IMPORT ROUTES
# ======================================
from routes import *
# ======================================
# CREATE DATABASE TABLES
# ======================================
with app.app_context():
    db.create_all()
# ======================================
# MAIN
# ======================================
if __name__ == '__main__':

    socketio.run(
        app,
        debug=True
    )