from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Notification, Student

notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')

@notifications_bp.route('', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get student's notifications"""
    try:
        student_id = get_jwt_identity()
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        query = Notification.query.filter(
            (Notification.student_id == student_id) | (Notification.student_id.is_(None))
        )
        
        if unread_only:
            query = query.filter_by(is_read=False)
        
        paginated = query.order_by(Notification.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        notifications = [notif.to_dict() for notif in paginated.items]
        
        return jsonify({
            'message': 'Notifications retrieved',
            'notifications': notifications,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notifications_bp.route('/<int:notification_id>', methods=['GET'])
@jwt_required()
def get_notification(notification_id):
    """Get single notification"""
    try:
        student_id = get_jwt_identity()
        
        notification = Notification.query.get(notification_id)
        
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
        
        # Check authorization
        if notification.student_id and notification.student_id != student_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({
            'message': 'Notification retrieved',
            'notification': notification.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notifications_bp.route('/<int:notification_id>/mark-read', methods=['PUT'])
@jwt_required()
def mark_as_read(notification_id):
    """Mark notification as read"""
    try:
        student_id = get_jwt_identity()
        
        notification = Notification.query.get(notification_id)
        
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
        
        # Check authorization
        if notification.student_id and notification.student_id != student_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        notification.is_read = True
        db.session.commit()
        
        return jsonify({
            'message': 'Notification marked as read',
            'notification': notification.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@notifications_bp.route('/mark-all-read', methods=['PUT'])
@jwt_required()
def mark_all_as_read():
    """Mark all notifications as read"""
    try:
        student_id = get_jwt_identity()
        
        Notification.query.filter(
            (Notification.student_id == student_id) | (Notification.student_id.is_(None)),
            Notification.is_read == False
        ).update({'is_read': True})
        
        db.session.commit()
        
        return jsonify({
            'message': 'All notifications marked as read'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@notifications_bp.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    """Delete a notification"""
    try:
        student_id = get_jwt_identity()
        
        notification = Notification.query.get(notification_id)
        
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
        
        # Check authorization
        if notification.student_id and notification.student_id != student_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        db.session.delete(notification)
        db.session.commit()
        
        return jsonify({
            'message': 'Notification deleted'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Admin endpoints

@notifications_bp.route('/admin/send', methods=['POST'])
@jwt_required()
def send_notification():
    """Send notification to students (Admin only)"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data.get('title') or not data.get('message'):
            return jsonify({'error': 'Title and message are required'}), 400
        
        # Send to specific student or broadcast
        if data.get('student_id'):
            notification = Notification(
                title=data['title'],
                message=data['message'],
                student_id=data['student_id']
            )
            db.session.add(notification)
        else:
            # Broadcast to all students
            students = Student.query.all()
            for student in students:
                notification = Notification(
                    title=data['title'],
                    message=data['message'],
                    student_id=student.id
                )
                db.session.add(notification)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Notification sent successfully'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@notifications_bp.route('/admin/broadcast', methods=['POST'])
@jwt_required()
def broadcast_notification():
    """Send broadcast notification to all students (Admin only)"""
    try:
        data = request.get_json()
        
        if not data.get('title') or not data.get('message'):
            return jsonify({'error': 'Title and message are required'}), 400
        
        # Create broadcast notification (no student_id means it goes to all)
        notification = Notification(
            title=data['title'],
            message=data['message'],
            student_id=None
        )
        
        db.session.add(notification)
        db.session.commit()
        
        return jsonify({
            'message': 'Broadcast notification sent successfully',
            'notification': notification.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@notifications_bp.route('/admin/all', methods=['GET'])
@jwt_required()
def get_all_notifications():
    """Get all notifications (Admin only)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        paginated = Notification.query.order_by(
            Notification.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        notifications = []
        for notif in paginated.items:
            data = notif.to_dict()
            if notif.student_id:
                student = Student.query.get(notif.student_id)
                data['student'] = student.to_dict() if student else None
            notifications.append(data)
        
        return jsonify({
            'message': 'Notifications retrieved',
            'notifications': notifications,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notifications_bp.route('/admin/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification_admin(notification_id):
    """Delete a notification (Admin only)"""
    try:
        notification = Notification.query.get(notification_id)
        
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
        
        db.session.delete(notification)
        db.session.commit()
        
        return jsonify({
            'message': 'Notification deleted'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
