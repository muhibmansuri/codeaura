from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models import db, Student
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Helper function to validate email
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Helper function to validate phone
def is_valid_phone(phone):
    pattern = r'^[0-9]{10}$'
    return re.match(pattern, phone) is not None

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new student"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data.get('name') or not data.get('email') or not data.get('password') or not data.get('phone'):
            return jsonify({'error': 'Name, email, password, and phone are required'}), 400
        
        if not is_valid_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if not is_valid_phone(data['phone']):
            return jsonify({'error': 'Phone must be 10 digits'}), 400
        
        # Check if student already exists
        if Student.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        if Student.query.filter_by(phone=data['phone']).first():
            return jsonify({'error': 'Phone number already registered'}), 400
        
        # Create new student
        student = Student(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            stream=data.get('stream'),
            age=data.get('age')
        )
        student.set_password(data['password'])
        
        db.session.add(student)
        db.session.commit()
        
        return jsonify({
            'message': 'Registration successful',
            'student': student.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login with email and password"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find student
        student = Student.query.filter_by(email=data['email']).first()
        
        if not student or not student.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create tokens
        access_token = create_access_token(identity=student.id)
        refresh_token = create_refresh_token(identity=student.id)
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'student': student.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login-phone', methods=['POST'])
def login_phone():
    """Login with phone number (OTP verification would be done on frontend)"""
    try:
        data = request.get_json()
        
        if not data.get('phone'):
            return jsonify({'error': 'Phone number is required'}), 400
        
        if not is_valid_phone(data['phone']):
            return jsonify({'error': 'Invalid phone number'}), 400
        
        # Find student
        student = Student.query.filter_by(phone=data['phone']).first()
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # In production, generate and send OTP via SMS
        # For now, return success
        return jsonify({
            'message': 'OTP sent to your phone',
            'phone': data['phone']
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """Verify OTP and generate tokens"""
    try:
        data = request.get_json()
        
        if not data.get('phone') or not data.get('otp'):
            return jsonify({'error': 'Phone and OTP are required'}), 400
        
        # In production, verify OTP with your SMS provider
        # For now, skip OTP verification in development
        
        student = Student.query.filter_by(phone=data['phone']).first()
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Create tokens
        access_token = create_access_token(identity=student.id)
        refresh_token = create_refresh_token(identity=student.id)
        
        return jsonify({
            'message': 'OTP verified successfully',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'student': student.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    try:
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        
        return jsonify({
            'message': 'Token refreshed',
            'access_token': access_token
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get student profile"""
    try:
        student_id = get_jwt_identity()
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        return jsonify({
            'message': 'Profile retrieved',
            'student': student.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update student profile"""
    try:
        student_id = get_jwt_identity()
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'name' in data:
            student.name = data['name']
        if 'stream' in data:
            student.stream = data['stream']
        if 'age' in data:
            student.age = data['age']
        if 'photo_url' in data:
            student.photo_url = data['photo_url']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'student': student.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change password"""
    try:
        student_id = get_jwt_identity()
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        data = request.get_json()
        
        if not data.get('old_password') or not data.get('new_password'):
            return jsonify({'error': 'Old and new passwords are required'}), 400
        
        if not student.check_password(data['old_password']):
            return jsonify({'error': 'Old password is incorrect'}), 401
        
        student.set_password(data['new_password'])
        db.session.commit()
        
        return jsonify({
            'message': 'Password changed successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
