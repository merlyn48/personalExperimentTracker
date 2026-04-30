from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from models.user import User
from extensions import db, bcrypt
from flask_jwt_extended import create_access_token
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__)

# --- Page routes (serve HTML) ---

@auth_bp.route('/')
def home():
    return render_template('home.html')

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

# --- Form POST handlers (browser form submissions) ---

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for('dashboard.dashboard'))

    flash('Invalid email or password.')
    return redirect(url_for('auth.login_page'))

@auth_bp.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')

    if User.query.filter_by(email=email).first():
        flash('Email already registered.')
        return redirect(url_for('auth.register_page'))

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(email=email, password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    flash('Registered successfully! Please log in.')
    return redirect(url_for('auth.login_page'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))

# --- JSON API routes (for programmatic access) ---

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({"token": token})
    return jsonify({"msg": "Invalid credentials"}), 401
