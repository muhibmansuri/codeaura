from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash
from models import db, Student, Course, Batch, Enrollment, Payment, Notification, Admin
from datetime import datetime, timedelta
from sqlalchemy import func
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')

# Admin login required decorator
def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please login first', 'danger')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            session['admin_role'] = admin.role
            flash(f'Welcome {admin.username}!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    """Admin logout"""
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@admin_login_required
def dashboard():
    """Dashboard with statistics"""
    try:
        # Get statistics
        total_students = Student.query.count()
        total_courses = Course.query.count()
        total_enrollments = Enrollment.query.count()
        active_enrollments = Enrollment.query.filter_by(status='active').count()
        
        # Payment stats
        total_payments = Payment.query.count()
        successful_payments = Payment.query.filter_by(status='success').count()
        pending_payments = Payment.query.filter_by(status='pending').count()
        total_revenue = db.session.query(func.sum(Payment.amount)).filter_by(status='success').scalar() or 0
        
        # Recent data
        recent_students = Student.query.order_by(Student.joined_date.desc()).limit(5).all()
        recent_enrollments = Enrollment.query.order_by(Enrollment.enrollment_date.desc()).limit(5).all()
        recent_payments = Payment.query.order_by(Payment.payment_date.desc()).limit(5).all()
        
        # Chart data
        enrollment_by_status = db.session.query(
            Enrollment.status,
            func.count(Enrollment.id)
        ).group_by(Enrollment.status).all()
        
        payment_by_status = db.session.query(
            Payment.status,
            func.count(Payment.id)
        ).group_by(Payment.status).all()
        
        return render_template('admin/dashboard.html',
            total_students=total_students,
            total_courses=total_courses,
            total_enrollments=total_enrollments,
            active_enrollments=active_enrollments,
            total_payments=total_payments,
            successful_payments=successful_payments,
            pending_payments=pending_payments,
            total_revenue=total_revenue,
            recent_students=recent_students,
            recent_enrollments=recent_enrollments,
            recent_payments=recent_payments,
            enrollment_by_status=enrollment_by_status,
            payment_by_status=payment_by_status
        )
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.login'))

@admin_bp.route('/students')
@admin_login_required
def students_list():
    """List all students"""
    try:
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '')
        
        query = Student.query
        
        if search:
            query = query.filter(
                (Student.name.ilike(f'%{search}%')) |
                (Student.email.ilike(f'%{search}%')) |
                (Student.phone.ilike(f'%{search}%'))
            )
        
        students = query.paginate(page=page, per_page=10, error_out=False)
        
        return render_template('admin/students.html',
            students=students,
            search=search
        )
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return render_template('admin/students.html', students=[], search='')

@admin_bp.route('/students/<int:student_id>')
@admin_login_required
def student_detail(student_id):
    """View student details"""
    try:
        student = Student.query.get(student_id)
        
        if not student:
            flash('Student not found', 'danger')
            return redirect(url_for('admin.students_list'))
        
        enrollments = Enrollment.query.filter_by(student_id=student_id).all()
        payments = Payment.query.filter_by(student_id=student_id).all()
        
        return render_template('admin/student_detail.html',
            student=student,
            enrollments=enrollments,
            payments=payments
        )
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.students_list'))

@admin_bp.route('/students/<int:student_id>/delete', methods=['POST'])
@admin_login_required
def delete_student(student_id):
    """Delete student"""
    try:
        student = Student.query.get(student_id)
        
        if not student:
            flash('Student not found', 'danger')
            return redirect(url_for('admin.students_list'))
        
        db.session.delete(student)
        db.session.commit()
        
        flash(f'Student {student.name} deleted', 'success')
        return redirect(url_for('admin.students_list'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.students_list'))

@admin_bp.route('/courses')
@admin_login_required
def courses_list():
    """List all courses"""
    try:
        page = request.args.get('page', 1, type=int)
        
        courses = Course.query.paginate(page=page, per_page=10, error_out=False)
        
        return render_template('admin/courses.html', courses=courses)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return render_template('admin/courses.html', courses=[])

@admin_bp.route('/courses/create', methods=['GET', 'POST'])
@admin_login_required
def create_course():
    """Create new course"""
    try:
        if request.method == 'POST':
            course = Course(
                name=request.form.get('name'),
                type=request.form.get('type'),
                fee=float(request.form.get('fee')),
                duration=request.form.get('duration'),
                image_url=request.form.get('image_url'),
                description=request.form.get('description'),
                syllabus=request.form.get('syllabus')
            )
            
            db.session.add(course)
            db.session.commit()
            
            flash(f'Course {course.name} created', 'success')
            return redirect(url_for('admin.courses_list'))
        
        return render_template('admin/course_form.html', course=None)
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
        return render_template('admin/course_form.html', course=None)

@admin_bp.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_login_required
def edit_course(course_id):
    """Edit course"""
    try:
        course = Course.query.get(course_id)
        
        if not course:
            flash('Course not found', 'danger')
            return redirect(url_for('admin.courses_list'))
        
        if request.method == 'POST':
            course.name = request.form.get('name')
            course.type = request.form.get('type')
            course.fee = float(request.form.get('fee'))
            course.duration = request.form.get('duration')
            course.image_url = request.form.get('image_url')
            course.description = request.form.get('description')
            course.syllabus = request.form.get('syllabus')
            
            db.session.commit()
            
            flash(f'Course {course.name} updated', 'success')
            return redirect(url_for('admin.courses_list'))
        
        return render_template('admin/course_form.html', course=course)
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.courses_list'))

@admin_bp.route('/courses/<int:course_id>/delete', methods=['POST'])
@admin_login_required
def delete_course(course_id):
    """Delete course"""
    try:
        course = Course.query.get(course_id)
        
        if not course:
            flash('Course not found', 'danger')
            return redirect(url_for('admin.courses_list'))
        
        db.session.delete(course)
        db.session.commit()
        
        flash(f'Course {course.name} deleted', 'success')
        return redirect(url_for('admin.courses_list'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.courses_list'))

@admin_bp.route('/batches')
@admin_login_required
def batches_list():
    """List all batches"""
    try:
        page = request.args.get('page', 1, type=int)
        course_id = request.args.get('course_id', type=int)
        
        query = Batch.query
        
        if course_id:
            query = query.filter_by(course_id=course_id)
        
        batches = query.paginate(page=page, per_page=10, error_out=False)
        courses = Course.query.all()
        
        return render_template('admin/batches.html',
            batches=batches,
            courses=courses,
            selected_course=course_id
        )
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return render_template('admin/batches.html', batches=[], courses=[])

@admin_bp.route('/batches/create', methods=['GET', 'POST'])
@admin_login_required
def create_batch():
    """Create new batch"""
    try:
        courses = Course.query.all()
        
        if request.method == 'POST':
            batch = Batch(
                batch_name=request.form.get('batch_name'),
                course_id=int(request.form.get('course_id')),
                timing=request.form.get('timing'),
                faculty=request.form.get('faculty'),
                start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else None
            )
            
            db.session.add(batch)
            db.session.commit()
            
            flash(f'Batch {batch.batch_name} created', 'success')
            return redirect(url_for('admin.batches_list'))
        
        return render_template('admin/batch_form.html', batch=None, courses=courses)
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
        return render_template('admin/batch_form.html', batch=None, courses=courses)

@admin_bp.route('/batches/<int:batch_id>/edit', methods=['GET', 'POST'])
@admin_login_required
def edit_batch(batch_id):
    """Edit batch"""
    try:
        batch = Batch.query.get(batch_id)
        courses = Course.query.all()
        
        if not batch:
            flash('Batch not found', 'danger')
            return redirect(url_for('admin.batches_list'))
        
        if request.method == 'POST':
            batch.batch_name = request.form.get('batch_name')
            batch.course_id = int(request.form.get('course_id'))
            batch.timing = request.form.get('timing')
            batch.faculty = request.form.get('faculty')
            batch.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else None
            
            db.session.commit()
            
            flash(f'Batch {batch.batch_name} updated', 'success')
            return redirect(url_for('admin.batches_list'))
        
        return render_template('admin/batch_form.html', batch=batch, courses=courses)
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.batches_list'))

@admin_bp.route('/batches/<int:batch_id>/delete', methods=['POST'])
@admin_login_required
def delete_batch(batch_id):
    """Delete batch"""
    try:
        batch = Batch.query.get(batch_id)
        
        if not batch:
            flash('Batch not found', 'danger')
            return redirect(url_for('admin.batches_list'))
        
        db.session.delete(batch)
        db.session.commit()
        
        flash(f'Batch {batch.batch_name} deleted', 'success')
        return redirect(url_for('admin.batches_list'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.batches_list'))

@admin_bp.route('/enrollments')
@admin_login_required
def enrollments_list():
    """List all enrollments"""
    try:
        page = request.args.get('page', 1, type=int)
        status = request.args.get('status')
        
        query = Enrollment.query
        
        if status:
            query = query.filter_by(status=status)
        
        enrollments = query.paginate(page=page, per_page=10, error_out=False)
        
        return render_template('admin/enrollments.html',
            enrollments=enrollments,
            selected_status=status
        )
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return render_template('admin/enrollments.html', enrollments=[])

@admin_bp.route('/enrollments/<int:enrollment_id>/update', methods=['POST'])
@admin_login_required
def update_enrollment(enrollment_id):
    """Update enrollment status"""
    try:
        enrollment = Enrollment.query.get(enrollment_id)
        
        if not enrollment:
            flash('Enrollment not found', 'danger')
            return redirect(url_for('admin.enrollments_list'))
        
        enrollment.status = request.form.get('status')
        db.session.commit()
        
        flash('Enrollment updated', 'success')
        return redirect(url_for('admin.enrollments_list'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.enrollments_list'))

@admin_bp.route('/payments')
@admin_login_required
def payments_list():
    """List all payments"""
    try:
        page = request.args.get('page', 1, type=int)
        status = request.args.get('status')
        
        query = Payment.query
        
        if status:
            query = query.filter_by(status=status)
        
        payments = query.paginate(page=page, per_page=10, error_out=False)
        
        return render_template('admin/payments.html',
            payments=payments,
            selected_status=status
        )
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return render_template('admin/payments.html', payments=[])

@admin_bp.route('/payments/<int:payment_id>/update', methods=['POST'])
@admin_login_required
def update_payment(payment_id):
    """Update payment status"""
    try:
        payment = Payment.query.get(payment_id)
        
        if not payment:
            flash('Payment not found', 'danger')
            return redirect(url_for('admin.payments_list'))
        
        payment.status = request.form.get('status')
        db.session.commit()
        
        flash('Payment updated', 'success')
        return redirect(url_for('admin.payments_list'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.payments_list'))

@admin_bp.route('/notifications')
@admin_login_required
def notifications_list():
    """List all notifications"""
    try:
        page = request.args.get('page', 1, type=int)
        
        notifications = Notification.query.paginate(page=page, per_page=10, error_out=False)
        
        return render_template('admin/notifications.html', notifications=notifications)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return render_template('admin/notifications.html', notifications=[])

@admin_bp.route('/notifications/send', methods=['GET', 'POST'])
@admin_login_required
def send_notification():
    """Send notification"""
    try:
        students = Student.query.all()
        
        if request.method == 'POST':
            student_id = request.form.get('student_id')
            
            if student_id:
                notification = Notification(
                    title=request.form.get('title'),
                    message=request.form.get('message'),
                    student_id=int(student_id)
                )
            else:
                notification = Notification(
                    title=request.form.get('title'),
                    message=request.form.get('message'),
                    student_id=None
                )
            
            db.session.add(notification)
            db.session.commit()
            
            flash('Notification sent', 'success')
            return redirect(url_for('admin.notifications_list'))
        
        return render_template('admin/notification_form.html', students=students)
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
        return render_template('admin/notification_form.html', students=students)

@admin_bp.route('/settings')
@admin_login_required
def settings():
    """Settings page"""
    return render_template('admin/settings.html')
