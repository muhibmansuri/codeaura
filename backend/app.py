import os
from flask import Flask, jsonify, session, redirect
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from models import db
from routes.auth import auth_bp
from routes.courses import courses_bp
from routes.admission import admission_bp
from routes.payments import payments_bp
from routes.notifications import notifications_bp
from routes.admin import admin_bp

def create_app(config_name=None):
    """Application factory"""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    jwt = JWTManager(app)
    
    # Configure session for admin panel
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = app.config.get('SECRET_KEY')
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(admission_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(admin_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Forbidden'}), 403
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'CodeAura Backend is running'
        }), 200
    
    # Admin panel redirect
    @app.route('/admin')
    def admin_redirect():
        return redirect('/admin/login')
    
    @app.route('/')
    def index():
        return jsonify({
            'message': 'CodeAura Backend API',
            'api': '/api',
            'admin': '/admin/login',
            'health': '/api/health'
        }), 200
    
    # API info endpoint
    @app.route('/api', methods=['GET'])
    def api_info():
        return jsonify({
            'name': 'CodeAura API',
            'version': '1.0.0',
            'description': 'Educational App Backend',
            'endpoints': {
                'auth': '/api/auth',
                'courses': '/api/courses',
                'admission': '/api/admission',
                'payments': '/api/payments',
                'notifications': '/api/notifications'
            }
        }), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
