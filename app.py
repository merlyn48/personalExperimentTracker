from flask import Flask
from config import config
from extensions import db, bcrypt, jwt, login_manager
from utils.reminders import mail

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # import models so db.create_all() sees them
    from models.user import User
    from models.experiment import Experiment
    from models.entry import Entry
    from models.tag import Tag

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # register blueprints
    from routes.auth_routes import auth_bp
    from routes.experiment_routes import exp_bp
    from routes.entry_routes import entry_bp
    from routes.dashboard_routes import dash_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(exp_bp)
    app.register_blueprint(entry_bp)
    app.register_blueprint(dash_bp)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
