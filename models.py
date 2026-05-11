from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """
    Requirement 3: PostgreSQL Integration for User Data [cite: 38-39]
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    # This links the user to their tasks
    tasks = db.relationship('Task', backref='owner', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Pending') # cite: 2
    deadline = db.Column(db.Date, nullable=True) # cite: 2
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))