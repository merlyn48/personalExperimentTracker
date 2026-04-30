from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.experiment import Experiment
from extensions import db

exp_bp = Blueprint('experiment', __name__)

@exp_bp.route('/experiment')
@login_required
def experiment_page():
    experiments = Experiment.query.filter_by(user_id=current_user.id).all()
    return render_template('experiment.html', experiments=experiments)

# FIX: stubs replaced with real DB logic
@exp_bp.route('/experiments', methods=['GET'])
@login_required
def get_experiments():
    experiments = Experiment.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        {"id": e.id, "name": e.name, "description": e.description, "is_active": e.is_active}
        for e in experiments
    ])

@exp_bp.route('/experiments', methods=['POST'])
@login_required
def create_experiment():
    data = request.get_json()
    exp = Experiment(
        name=data['name'],
        description=data.get('description', ''),
        user_id=current_user.id
    )
    db.session.add(exp)
    db.session.commit()
    return jsonify({"msg": "Experiment created", "id": exp.id}), 201

@exp_bp.route('/experiments/<int:exp_id>', methods=['DELETE'])
@login_required
def delete_experiment(exp_id):
    exp = Experiment.query.filter_by(id=exp_id, user_id=current_user.id).first_or_404()
    db.session.delete(exp)
    db.session.commit()
    return jsonify({"msg": "Experiment deleted"})
