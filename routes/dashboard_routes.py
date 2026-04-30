from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.experiment import Experiment
from datetime import date

dash_bp = Blueprint('dashboard', __name__)

@dash_bp.route('/dashboard')
@login_required
def dashboard():
    experiments = Experiment.query.filter_by(user_id=current_user.id).all()
    total = len(experiments)

    # Count entries logged today
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

@dash_bp.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html')
