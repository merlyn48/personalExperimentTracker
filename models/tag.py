from extensions import db

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id'))
