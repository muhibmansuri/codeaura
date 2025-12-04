from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Student, Enrollment, Batch, Course
from datetime import datetime

admission_bp = Blueprint('admission', __name__, url_prefix='/api/admission')

@admission_bp.route('/enroll', methods=['POST'])
@jwt_required()
def enroll_course():
    """Enroll student in a batch"""
    try:
        student_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate input
        if not data.get('batch_id'):
            return jsonify({'error': 'Batch ID is required'}), 400
        
        # Check student exists
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Check batch exists
        batch = Batch.query.get(data['batch_id'])
        if not batch:
            return jsonify({'error': 'Batch not found'}), 404
        
        # Check if already enrolled
        existing_enrollment = Enrollment.query.filter_by(
            student_id=student_id,
            batch_id=data['batch_id']
        ).first()
        
        if existing_enrollment:
            return jsonify({'error': 'Already enrolled in this batch'}), 400
        
        # Create enrollment
        enrollment = Enrollment(
            student_id=student_id,
            batch_id=data['batch_id'],
            status='active'
        )
        
        db.session.add(enrollment)
        db.session.commit()
        
        return jsonify({
            'message': 'Enrollment successful',
            'enrollment': enrollment.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admission_bp.route('/my-enrollments', methods=['GET'])
@jwt_required()
def get_my_enrollments():
    """Get student's enrollments"""
    try:
        student_id = get_jwt_identity()
        
        enrollments = Enrollment.query.filter_by(student_id=student_id).all()
        
        enrollment_data = []
        for enrollment in enrollments:
            batch = Batch.query.get(enrollment.batch_id)
            course = Course.query.get(batch.course_id)
            
            data = enrollment.to_dict()
            data['batch'] = batch.to_dict()
            data['course'] = course.to_dict()
            enrollment_data.append(data)
        
        return jsonify({
            'message': 'Enrollments retrieved',
            'enrollments': enrollment_data
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admission_bp.route('/enrollments/<int:enrollment_id>', methods=['GET'])
@jwt_required()
def get_enrollment_details(enrollment_id):
    """Get enrollment details"""
    try:
        student_id = get_jwt_identity()
        
        enrollment = Enrollment.query.get(enrollment_id)
        
        if not enrollment:
            return jsonify({'error': 'Enrollment not found'}), 404
        
        # Check if enrollment belongs to user
        if enrollment.student_id != student_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        batch = Batch.query.get(enrollment.batch_id)
        course = Course.query.get(batch.course_id)
        
        data = enrollment.to_dict()
        data['batch'] = batch.to_dict()
        data['course'] = course.to_dict()
        
        return jsonify({
            'message': 'Enrollment details retrieved',
            'enrollment': data
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admission_bp.route('/enrollments/<int:enrollment_id>/status', methods=['PUT'])
@jwt_required()
def update_enrollment_status(enrollment_id):
    """Update enrollment status (Admin only)"""
    try:
        enrollment = Enrollment.query.get(enrollment_id)
        
        if not enrollment:
            return jsonify({'error': 'Enrollment not found'}), 404
        
        data = request.get_json()
        
        if not data.get('status'):
            return jsonify({'error': 'Status is required'}), 400
        
        valid_statuses = ['active', 'completed', 'dropped']
        if data['status'] not in valid_statuses:
            return jsonify({'error': f'Status must be one of {valid_statuses}'}), 400
        
        enrollment.status = data['status']
        db.session.commit()
        
        return jsonify({
            'message': 'Enrollment status updated',
            'enrollment': enrollment.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admission_bp.route('/enrollments/<int:enrollment_id>', methods=['DELETE'])
@jwt_required()
def unenroll(enrollment_id):
    """Unenroll from a course"""
    try:
        student_id = get_jwt_identity()
        
        enrollment = Enrollment.query.get(enrollment_id)
        
        if not enrollment:
            return jsonify({'error': 'Enrollment not found'}), 404
        
        # Check if enrollment belongs to user
        if enrollment.student_id != student_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        db.session.delete(enrollment)
        db.session.commit()
        
        return jsonify({
            'message': 'Unenrolled successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Admin endpoints for enrollment management

@admission_bp.route('/admin/enrollments', methods=['GET'])
@jwt_required()
def get_all_enrollments():
    """Get all enrollments (Admin only)"""
    try:
        student_id = request.args.get('student_id', type=int)
        batch_id = request.args.get('batch_id', type=int)
        status = request.args.get('status')
        
        query = Enrollment.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        
        if batch_id:
            query = query.filter_by(batch_id=batch_id)
        
        if status:
            query = query.filter_by(status=status)
        
        enrollments = query.all()
        
        enrollment_data = []
        for enrollment in enrollments:
            student = Student.query.get(enrollment.student_id)
            batch = Batch.query.get(enrollment.batch_id)
            course = Course.query.get(batch.course_id)
            
            data = enrollment.to_dict()
            data['student'] = student.to_dict()
            data['batch'] = batch.to_dict()
            data['course'] = course.to_dict()
            enrollment_data.append(data)
        
        return jsonify({
            'message': 'Enrollments retrieved',
            'enrollments': enrollment_data,
            'total': len(enrollment_data)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admission_bp.route('/admin/batches', methods=['GET'])
@jwt_required()
def get_batches():
    """Get all batches (Admin)"""
    try:
        course_id = request.args.get('course_id', type=int)
        
        query = Batch.query
        
        if course_id:
            query = query.filter_by(course_id=course_id)
        
        batches = query.all()
        
        batch_data = [batch.to_dict() for batch in batches]
        
        return jsonify({
            'message': 'Batches retrieved',
            'batches': batch_data
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admission_bp.route('/admin/batches', methods=['POST'])
@jwt_required()
def create_batch():
    """Create a new batch (Admin only)"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data.get('batch_name') or not data.get('course_id'):
            return jsonify({'error': 'Batch name and course ID are required'}), 400
        
        # Check course exists
        course = Course.query.get(data['course_id'])
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        batch = Batch(
            batch_name=data['batch_name'],
            course_id=data['course_id'],
            timing=data.get('timing'),
            faculty=data.get('faculty'),
            start_date=datetime.fromisoformat(data['start_date']) if data.get('start_date') else None
        )
        
        db.session.add(batch)
        db.session.commit()
        
        return jsonify({
            'message': 'Batch created successfully',
            'batch': batch.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admission_bp.route('/admin/batches/<int:batch_id>', methods=['PUT'])
@jwt_required()
def update_batch(batch_id):
    """Update a batch (Admin only)"""
    try:
        batch = Batch.query.get(batch_id)
        
        if not batch:
            return jsonify({'error': 'Batch not found'}), 404
        
        data = request.get_json()
        
        if 'batch_name' in data:
            batch.batch_name = data['batch_name']
        if 'timing' in data:
            batch.timing = data['timing']
        if 'faculty' in data:
            batch.faculty = data['faculty']
        if 'start_date' in data:
            batch.start_date = datetime.fromisoformat(data['start_date'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Batch updated successfully',
            'batch': batch.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admission_bp.route('/admin/batches/<int:batch_id>', methods=['DELETE'])
@jwt_required()
def delete_batch(batch_id):
    """Delete a batch (Admin only)"""
    try:
        batch = Batch.query.get(batch_id)
        
        if not batch:
            return jsonify({'error': 'Batch not found'}), 404
        
        db.session.delete(batch)
        db.session.commit()
        
        return jsonify({
            'message': 'Batch deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
