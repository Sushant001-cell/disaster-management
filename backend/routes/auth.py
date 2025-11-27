"""
Authentication routes - signup, login, logout
"""
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, UserRole

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """User signup endpoint"""
    data = request.get_json()
    
    # Validate input
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        return {'error': 'Missing required fields'}, 400
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return {'error': 'Email already registered'}, 409
    
    # Create new user
    user = User(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        location=data.get('location'),
        role=UserRole[data.get('role', 'CITIZEN').upper()]
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return {
        'message': 'User created successfully',
        'user': user.to_dict()
    }, 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return {'error': 'Missing email or password'}, 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return {'error': 'Invalid email or password'}, 401
    
    if not user.is_active:
        return {'error': 'Account is inactive'}, 403
    
    login_user(user)
    
    return {
        'message': 'Login successful',
        'user': user.to_dict()
    }, 200


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """User logout endpoint"""
    logout_user()
    return {'message': 'Logged out successfully'}, 200


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current user info"""
    return current_user.to_dict(), 200
