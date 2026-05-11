# Smart Task Management System

A modern Flask-based task management web application developed as part of a Python Development Internship Assignment.

The application allows users to manage tasks efficiently with real-time updates, analytics, deadline tracking, and workflow visualization.

---

# Features

## Authentication
- User Registration
- User Login
- Logout Functionality
- Password Hashing for Security

## Task Management
- Add Tasks
- Delete Tasks
- Update Task Status
- Pending & Completed Sections
- Priority Levels (High, Medium, Low)
- Deadline Support
- Task Search & Filters

## Analytics Dashboard
- Total Tasks
- Completed Tasks
- Pending Tasks
- Completion Percentage
- Doughnut Chart Visualization
- Priority Heatmap

## Real-Time Features
- WebSocket Integration using Flask-SocketIO
- Live Dashboard Updates
- Instant Task Refresh

## Notifications
- Overdue Task Alerts
- Due Today Notifications
- Due Tomorrow Notifications

## UI Features
- Responsive Dashboard
- Collapsible Sidebar
- Modern Card Design
- Interactive Charts
- Workflow Efficiency Messages

---

# Technologies Used

- Python
- Flask
- PostgreSQL
- Flask-SQLAlchemy
- Flask-Login
- Flask-SocketIO
- Pandas
- NumPy
- HTML
- CSS
- Bootstrap 5
- JavaScript
- Chart.js

---

# Project Structure

```text
project/
│
├── static/
├── templates/
├── app.py
├── models.py
├── routes.py
├── requirements.txt
├── README.md
└── .env


Installation Steps
1. Clone Repository
git clone YOUR_GITHUB_LINK

2. Navigate to Project
cd smart-task-manager

3. Create Virtual Environment
python -m venv venv

4. Activate Virtual Environment
Windows
venv\Scripts\activate
Mac/Linux
source venv/bin/activate

5. Install Dependencies
pip install -r requirements.txt

6. Configure PostgreSQL
Create PostgreSQL database and update DATABASE_URL in .env.

7. Run Application
python app.py
