from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Course, Batch, Video, Note, Test
from sqlalchemy import or_

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

@courses_bp.route('', methods=['GET'])
def get_courses():
    """Get all courses with optional filters"""
    try:
        # Get query parameters
        course_type = request.args.get('type')
        duration = request.args.get('duration')
        search = request.args.get('search')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Build query
        query = Course.query
        
        # Apply filters
        if course_type:
            query = query.filter_by(type=course_type)
        
        if duration:
            query = query.filter_by(duration=duration)
        
        if search:
            query = query.filter(
                or_(
                    Course.name.ilike(f'%{search}%'),
                    Course.description.ilike(f'%{search}%')
                )
            )
        
        # Paginate
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        courses = [course.to_dict() for course in paginated.items]
        
        return jsonify({
            'message': 'Courses retrieved',
            'courses': courses,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/<int:course_id>', methods=['GET'])
def get_course_details(course_id):
    """Get course details with batches"""
    try:
        course = Course.query.get(course_id)
        
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        course_data = course.to_dict()
        course_data['batches'] = [batch.to_dict() for batch in course.batches]
        course_data['video_count'] = len(course.videos)
        course_data['note_count'] = len(course.notes)
        course_data['test_count'] = len(course.tests)
        
        return jsonify({
            'message': 'Course details retrieved',
            'course': course_data
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/<int:course_id>/videos', methods=['GET'])
def get_course_videos(course_id):
    """Get videos for a course"""
    try:
        course = Course.query.get(course_id)
        
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        videos = [video.to_dict() for video in course.videos]
        
        return jsonify({
            'message': 'Videos retrieved',
            'videos': videos
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/<int:course_id>/notes', methods=['GET'])
def get_course_notes(course_id):
    """Get notes for a course"""
    try:
        course = Course.query.get(course_id)
        
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        notes = [note.to_dict() for note in course.notes]
        
        return jsonify({
            'message': 'Notes retrieved',
            'notes': notes
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/<int:course_id>/tests', methods=['GET'])
def get_course_tests(course_id):
    """Get tests for a course"""
    try:
        course = Course.query.get(course_id)
        
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        tests = [test.to_dict() for test in course.tests]
        
        return jsonify({
            'message': 'Tests retrieved',
            'tests': tests
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin endpoints for course management

@courses_bp.route('', methods=['POST'])
@jwt_required()
def create_course():
    """Create a new course (Admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('type') or data.get('fee') is None:
            return jsonify({'error': 'Name, type, and fee are required'}), 400
        
        course = Course(
            name=data['name'],
            type=data['type'],
            fee=data['fee'],
            duration=data.get('duration'),
            image_url=data.get('image_url'),
            description=data.get('description'),
            syllabus=data.get('syllabus')
        )
        
        db.session.add(course)
        db.session.commit()
        
        return jsonify({
            'message': 'Course created successfully',
            'course': course.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/<int:course_id>', methods=['PUT'])
@jwt_required()
def update_course(course_id):
    """Update a course (Admin only)"""
    try:
        course = Course.query.get(course_id)
        
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            course.name = data['name']
        if 'type' in data:
            course.type = data['type']
        if 'fee' in data:
            course.fee = data['fee']
        if 'duration' in data:
            course.duration = data['duration']
        if 'image_url' in data:
            course.image_url = data['image_url']
        if 'description' in data:
            course.description = data['description']
        if 'syllabus' in data:
            course.syllabus = data['syllabus']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Course updated successfully',
            'course': course.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@courses_bp.route('/<int:course_id>', methods=['DELETE'])
@jwt_required()
def delete_course(course_id):
    """Delete a course (Admin only)"""
    try:
        course = Course.query.get(course_id)
        
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        db.session.delete(course)
        db.session.commit()
        
        return jsonify({
            'message': 'Course deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Video endpoints

@courses_bp.route('/<int:course_id>/videos', methods=['POST'])
@jwt_required()
def create_video(course_id):
    """Add video to course (Admin only)"""
    try:
        course = Course.query.get(course_id)
        
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        data = request.get_json()
        
        if not data.get('title') or not data.get('video_url'):
            return jsonify({'error': 'Title and video URL are required'}), 400
        
        video = Video(
            course_id=course_id,
            title=data['title'],
            video_url=data['video_url'],
            duration=data.get('duration'),
            description=data.get('description')
        )
        
        db.session.add(video)
        db.session.commit()
        
        return jsonify({
            'message': 'Video added successfully',
            'video': video.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Note endpoints

@courses_bp.route('/<int:course_id>/notes', methods=['POST'])
@jwt_required()
def create_note(course_id):
    """Add note to course (Admin only)"""
    try:
        course = Course.query.get(course_id)
        
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        data = request.get_json()
        
        if not data.get('title') or not data.get('pdf_url'):
            return jsonify({'error': 'Title and PDF URL are required'}), 400
        
        note = Note(
            course_id=course_id,
            title=data['title'],
            pdf_url=data['pdf_url']
        )
        
        db.session.add(note)
        db.session.commit()
        
        return jsonify({
            'message': 'Note added successfully',
            'note': note.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Test endpoints

@courses_bp.route('/<int:course_id>/tests', methods=['POST'])
@jwt_required()
def create_test(course_id):
    """Add test to course (Admin only)"""
    try:
        course = Course.query.get(course_id)
        
        if not course:
            return jsonify({'error': 'Course not found'}), 404
        
        data = request.get_json()
        
        if not data.get('title') or not data.get('questions_json'):
            return jsonify({'error': 'Title and questions are required'}), 400
        
        test = Test(
            course_id=course_id,
            title=data['title'],
            questions_json=data['questions_json'],
            duration=data.get('duration'),
            passing_score=data.get('passing_score')
        )
        
        db.session.add(test)
        db.session.commit()
        
        return jsonify({
            'message': 'Test added successfully',
            'test': test.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
