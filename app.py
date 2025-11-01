"""
FFCX Timetable Application - Modular Flask Backend
This file serves as the main application entry point using modular components.
"""

from flask import Flask, request, jsonify, render_template
import os
import sys

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import modular components
from config.timetable_config import TIMETABLE_TEMPLATE, COURSE_INFO
from helpers.data_loader import load_teachers_from_csv, load_courses_from_ref2
from helpers.time_utils import generate_slot_conflicts, parse_time_range, get_conflict_details
from features.validation import validate_priority_conflicts
from features.optimization import optimize_timetable_logic

# Import route modules
from routes.basic_routes import register_basic_routes
from routes.course_routes import register_course_routes
from routes.validation_routes import register_validation_routes
from routes.course_management_routes import register_course_management_routes
from routes.optimization_routes import register_optimization_routes
from routes.export_import_routes import register_export_import_routes

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ffcx-timetable-secret-key-2024')
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Initialize global application state
    app.timetable = TIMETABLE_TEMPLATE.copy()
    app.enrolled_courses = []
    app.all_teachers = []
    app.all_courses = []
    
    # Load initial data
    load_initial_data(app)
    
    # Register all route modules
    register_routes(app)
    
    # Error handlers
    register_error_handlers(app)
    
    return app

def load_initial_data(app):
    """Load initial data from CSV files."""
    try:
        # Load teachers data
        app.all_teachers = load_teachers_from_csv('all_teachers.csv')
        print(f"Loaded {len(app.all_teachers)} teachers")
        
        # Load courses data
        app.all_courses = load_courses_from_ref2('ref2.txt')
        print(f"Loaded {len(app.all_courses)} courses")
        
    except Exception as e:
        print(f"Error loading initial data: {e}")
        # Initialize with empty data if files are missing
        app.all_teachers = []
        app.all_courses = []

def register_routes(app):
    """Register all route modules with the Flask app."""
    try:
        register_basic_routes(app)
        register_course_routes(app)
        register_validation_routes(app)
        register_course_management_routes(app)
        register_optimization_routes(app)
        register_export_import_routes(app)
        
        print("All routes registered successfully")
        
    except Exception as e:
        print(f"Error registering routes: {e}")
        raise

def register_error_handlers(app):
    """Register global error handlers."""
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors."""
        if request.is_json:
            return jsonify({
                'success': False,
                'message': 'Resource not found',
                'error_code': 404
            }), 404
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        if request.is_json:
            return jsonify({
                'success': False,
                'message': 'Internal server error',
                'error_code': 500
            }), 500
        return render_template('500.html'), 500
    
    @app.errorhandler(400)
    def bad_request_error(error):
        """Handle 400 errors."""
        if request.is_json:
            return jsonify({
                'success': False,
                'message': 'Bad request',
                'error_code': 400
            }), 400
        return jsonify({'success': False, 'message': 'Bad request'}), 400

def setup_cors(app):
    """Setup CORS headers for API endpoints."""
    @app.after_request
    def after_request(response):
        """Add CORS headers to all responses."""
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

def setup_logging(app):
    """Setup application logging."""
    import logging
    from logging.handlers import RotatingFileHandler
    
    if not app.debug:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Setup file handler with rotation
        file_handler = RotatingFileHandler('logs/ffcx.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('FFCX Timetable startup')

# Create the Flask application
app = create_app()

# Setup additional configurations
setup_cors(app)
setup_logging(app)

# Add utility functions to app context
@app.context_processor
def utility_processor():
    """Make utility functions available in templates."""
    return {
        'enumerate': enumerate,
        'len': len,
        'str': str,
        'int': int,
        'float': float,
        'bool': bool,
    }

# CLI commands for development
@app.cli.command()
def init_db():
    """Initialize the database (if using one in the future)."""
    print("Database initialization would go here")

@app.cli.command()
def load_sample_data():
    """Load sample data for testing."""
    try:
        load_initial_data(app)
        print("Sample data loaded successfully")
    except Exception as e:
        print(f"Error loading sample data: {e}")

@app.cli.command()
def clear_data():
    """Clear all timetable data."""
    app.timetable = TIMETABLE_TEMPLATE.copy()
    app.enrolled_courses = []
    print("All data cleared")

# Development server configuration
if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Starting FFCX Timetable Application on {host}:{port}")
    print(f"Debug mode: {debug}")
    
    # Run the development server
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )