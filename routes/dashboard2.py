from flask import Blueprint, render_template

dash_bp = Blueprint('dashboard', __name__)

@dash_bp.route('/')
def home():
    return render_template('home.html')
