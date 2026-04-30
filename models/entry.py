from extensions import db
from datetime import date

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    # FIX: changed DateTime to Date so comparison with date.today() in reminders.py works
    date = db.Column(db.Date, default=date.today)

    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id'), nullable=False)
