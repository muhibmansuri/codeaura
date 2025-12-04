from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Student, Payment
import razorpay

payments_bp = Blueprint('payments', __name__, url_prefix='/api/payments')

# Initialize Razorpay client (use your keys from config)
# In production, use app config
razorpay_client = None

def init_razorpay(key_id, key_secret):
    global razorpay_client
    razorpay_client = razorpay.Client(auth=(key_id, key_secret))

@payments_bp.route('/create', methods=['POST'])
@jwt_required()
def create_payment():
    """Create a payment order"""
    try:
        student_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate input
        if not data.get('amount') or not data.get('method'):
            return jsonify({'error': 'Amount and method are required'}), 400
        
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Create payment record
        payment = Payment(
            student_id=student_id,
            amount=data['amount'],
            method=data['method'],
            status='pending'
        )
        
        # If Razorpay method, create order
        if data['method'] == 'razorpay' and razorpay_client:
            try:
                order = razorpay_client.order.create({
                    'amount': int(data['amount'] * 100),  # Amount in paise
                    'currency': 'INR',
                    'receipt': f'receipt#{student_id}#{int(payment.id)}',
                    'payment_capture': 1
                })
                
                payment.razorpay_payment_id = order['id']
                
                db.session.add(payment)
                db.session.commit()
                
                return jsonify({
                    'message': 'Payment order created',
                    'order_id': order['id'],
                    'amount': data['amount'],
                    'currency': 'INR',
                    'payment': payment.to_dict()
                }), 201
            
            except Exception as e:
                return jsonify({'error': f'Razorpay error: {str(e)}'}), 500
        
        # For other methods
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({
            'message': 'Payment created',
            'payment': payment.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/verify', methods=['POST'])
@jwt_required()
def verify_payment():
    """Verify payment after completion"""
    try:
        student_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('payment_id') or not data.get('order_id'):
            return jsonify({'error': 'Payment ID and Order ID are required'}), 400
        
        if razorpay_client:
            try:
                # Verify payment signature
                payment_details = razorpay_client.payment.fetch(data['payment_id'])
                
                if payment_details['status'] == 'captured':
                    # Update payment status
                    payment = Payment.query.filter_by(
                        student_id=student_id,
                        razorpay_payment_id=data['order_id']
                    ).first()
                    
                    if payment:
                        payment.status = 'success'
                        payment.razorpay_payment_id = data['payment_id']
                        db.session.commit()
                        
                        return jsonify({
                            'message': 'Payment verified successfully',
                            'payment': payment.to_dict()
                        }), 200
            
            except Exception as e:
                return jsonify({'error': f'Verification failed: {str(e)}'}), 500
        
        return jsonify({'error': 'Payment verification failed'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/history', methods=['GET'])
@jwt_required()
def get_payment_history():
    """Get student's payment history"""
    try:
        student_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        paginated = Payment.query.filter_by(student_id=student_id).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        payments = [payment.to_dict() for payment in paginated.items]
        
        return jsonify({
            'message': 'Payment history retrieved',
            'payments': payments,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/<int:payment_id>', methods=['GET'])
@jwt_required()
def get_payment_details(payment_id):
    """Get payment details"""
    try:
        student_id = get_jwt_identity()
        
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        
        # Check if payment belongs to user
        if payment.student_id != student_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({
            'message': 'Payment details retrieved',
            'payment': payment.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin endpoints

@payments_bp.route('/admin/all', methods=['GET'])
@jwt_required()
def get_all_payments():
    """Get all payments (Admin only)"""
    try:
        student_id = request.args.get('student_id', type=int)
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        query = Payment.query
        
        if student_id:
            query = query.filter_by(student_id=student_id)
        
        if status:
            query = query.filter_by(status=status)
        
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        payments = []
        for payment in paginated.items:
            data = payment.to_dict()
            student = Student.query.get(payment.student_id)
            data['student'] = student.to_dict()
            payments.append(data)
        
        return jsonify({
            'message': 'Payments retrieved',
            'payments': payments,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': paginated.total,
                'pages': paginated.pages
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/admin/dashboard', methods=['GET'])
@jwt_required()
def get_payment_dashboard():
    """Get payment dashboard statistics (Admin only)"""
    try:
        from sqlalchemy import func
        
        total_payments = Payment.query.with_entities(func.count(Payment.id)).scalar()
        total_amount = Payment.query.with_entities(func.sum(Payment.amount)).scalar()
        successful_payments = Payment.query.filter_by(status='success').with_entities(func.count(Payment.id)).scalar()
        pending_payments = Payment.query.filter_by(status='pending').with_entities(func.count(Payment.id)).scalar()
        failed_payments = Payment.query.filter_by(status='failed').with_entities(func.count(Payment.id)).scalar()
        
        return jsonify({
            'message': 'Dashboard stats retrieved',
            'stats': {
                'total_payments': total_payments,
                'total_amount': total_amount or 0,
                'successful_payments': successful_payments,
                'pending_payments': pending_payments,
                'failed_payments': failed_payments
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/admin/<int:payment_id>/update-status', methods=['PUT'])
@jwt_required()
def update_payment_status(payment_id):
    """Update payment status (Admin only)"""
    try:
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        
        data = request.get_json()
        
        if not data.get('status'):
            return jsonify({'error': 'Status is required'}), 400
        
        valid_statuses = ['success', 'pending', 'failed']
        if data['status'] not in valid_statuses:
            return jsonify({'error': f'Status must be one of {valid_statuses}'}), 400
        
        payment.status = data['status']
        db.session.commit()
        
        return jsonify({
            'message': 'Payment status updated',
            'payment': payment.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/admin/<int:payment_id>', methods=['DELETE'])
@jwt_required()
def delete_payment(payment_id):
    """Delete a payment record (Admin only)"""
    try:
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        
        db.session.delete(payment)
        db.session.commit()
        
        return jsonify({
            'message': 'Payment deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
