from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.entry import Entry
from models.experiment import Experiment
from extensions import db
from datetime import date

entry_bp = Blueprint('entry', __name__)

# FIX: stub replaced with real DB logic
@entry_bp.route('/entries', methods=['POST'])
@login_required
def add_entry():
    data = request.get_json()
    exp_id = data.get('experiment_id')

    # Verify the experiment belongs to the current user
    exp = Experiment.query.filter_by(id=exp_id, user_id=current_user.id).first_or_404()

    entry = Entry(
        content=data.get('content', ''),
        experiment_id=exp.id,
        date=date.today()
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify({"msg": "Entry added", "id": entry.id}), 201

@entry_bp.route('/entries/<int:exp_id>', methods=['GET'])
@login_required
def get_entries(exp_id):
    exp = Experiment.query.filter_by(id=exp_id, user_id=current_user.id).first_or_404()
    entries = [{"id": e.id, "content": e.content, "date": str(e.date)} for e in exp.entries]
    return jsonify(entries)
