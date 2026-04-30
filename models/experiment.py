from extensions import db

class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # FIX: added 'name' field (was 'title') to match reminders.py usage
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    # FIX: added is_active field required by reminders.py
    is_active = db.Column(db.Boolean, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    entries = db.relationship('Entry', backref='experiment', lazy=True)
    tags = db.relationship('Tag', backref='experiment', lazy=True)
