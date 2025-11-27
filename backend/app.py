"""
Main Flask Application for Disaster Management System
"""
import os
import tempfile
from flask import Flask, request
from flask_cors import CORS
from flask_login import LoginManager
from flask_socketio import SocketIO
from dotenv import load_dotenv
from models import db, User, UserRole, init_db

# Load environment variables
load_dotenv()

# Initialize extensions
socketio = SocketIO()
login_manager = LoginManager()


def create_app(config_name='development'):
    """Application factory"""
    # Set up static file paths for frontend
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    database_path = os.path.join(base_path, 'database')
    
    # Create database directory if it doesn't exist
    os.makedirs(database_path, exist_ok=True)
    
    app = Flask(__name__, static_folder=frontend_path, static_url_path='')

    # Register centralized error handlers early so they catch errors during initialization
    try:
        from error_handlers import register_error_handlers
        register_error_handlers(app)
    except Exception:
        import traceback as _tb
        print('Failed to register error handlers early:', _tb.format_exc())
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-this')
    
    # Handle DATABASE_URL: if set, use it directly; otherwise use temp directory
    # This avoids OneDrive file locking issues
    if os.getenv('DATABASE_URL'):
        db_uri = os.getenv('DATABASE_URL')
    else:
        # Use system temp directory for better compatibility on Windows
        temp_dir = tempfile.gettempdir()
        db_file = os.path.join(temp_dir, 'disaster_mgmt.db')
        # Create proper SQLite URI
        db_uri = f'sqlite:///{db_file.replace(chr(92), "/")}'
    
    print(f'[DEBUG] Database URI: {db_uri}')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    
    # Initialize extensions
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    socketio.init_app(app, cors_allowed_origins='*')
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    # Register blueprints
    from routes import auth_bp, admin_bp, citizen_bp, volunteer_bp, api_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(citizen_bp)
    app.register_blueprint(volunteer_bp)
    app.register_blueprint(api_bp)
    
    # (error handlers already registered early)
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(403)
    def forbidden(error):
        return {'error': 'Access forbidden'}, 403
    
    @app.route('/api/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return {'status': 'ok', 'message': 'Disaster Management System is running'}, 200
    
    @app.route('/')
    def serve_index():
        """Serve the frontend index.html"""
        from flask import send_from_directory
        return send_from_directory(frontend_path, 'index.html')
    
    # Initialize database on first request (but skip for health check)
    @app.before_request
    def initialize_db():
        # Skip DB initialization for health check endpoint
        if request.path == '/api/health':
            return
        
        if not hasattr(app, 'db_initialized'):
            try:
                # Ensure the database directory exists (if using file-based SQLite)
                db_uri = app.config['SQLALCHEMY_DATABASE_URI']
                if db_uri.startswith('sqlite:///'):
                    db_file = db_uri.replace('sqlite:///', '')
                    db_dir = os.path.dirname(db_file)
                    if db_dir:
                        os.makedirs(db_dir, exist_ok=True)
                
                print(f'Initializing database: {db_uri}')
                db.create_all()
                
                # Create default admin user if it doesn't exist
                admin = User.query.filter_by(email='admin@disaster.com').first()
                if not admin:
                    admin = User(
                        name='Admin',
                        email='admin@disaster.com',
                        phone='9999999999',
                        role=UserRole.ADMIN,
                        is_active=True
                    )
                    admin.set_password('admin123')
                    db.session.add(admin)
                    db.session.commit()
                
                app.db_initialized = True
                print('Database initialized successfully')
            except Exception as e:
                print(f'Error initializing database: {e}')
                import traceback
                traceback.print_exc()
                raise
    
    return app


# Create app instance
app = create_app()


if __name__ == '__main__':
    # Development server (use Gunicorn for production)
    # Note: Not using socketio.run() on Windows due to eventlet port binding issues
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=False
    )
