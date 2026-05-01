from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from models.experiment import Experiment
from models.user import User
from models.entry import Entry
from datetime import date

dash_bp = Blueprint('dashboard', __name__)

# 🔹 Home route
@dash_bp.route('/')
def home():
    return render_template('home.html')


# 🔹 Dashboard
@dash_bp.route('/dashboard')
@login_required
def dashboard():
    experiments = Experiment.query.filter_by(user_id=current_user.id).all()
    total = len(experiments)

    today = date.today()
    logged_today = [
        e for exp in experiments
        for e in exp.entries
        if e.date == today
    ]

    return render_template(
        'dashboard.html',
        experiments=experiments,
        total=total,
        logged_today=logged_today
    )


# 🔹 Analytics
@dash_bp.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html')


# 🔹 Test DB route (safe version)
@dash_bp.route('/test-db')
def test_db():
    try:
        users = User.query.all()
        experiments = Experiment.query.all()
        entries = Entry.query.all()

        return jsonify({
            "users": [u.email for u in users],
            "experiments": [e.title if e.title else "No Title" for e in experiments],
            "entries": [e.content if e.content else "No Content" for e in entries]
        })
    except Exception as e:
        return jsonify({"error": str(e)})
