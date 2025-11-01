


from flask import Flask
from config.timetable_config import get_timetable

app = Flask(__name__)

@app.route('/')
def index():
    timetable = get_timetable()
    html = "<h1>FFCX Timetable</h1>"
    for day, slots in timetable.items():
        html += f"<h2>{day}</h2><ul>"
        for slot in slots:
            html += f"<li>{slot['hour']}</li>"
        html += "</ul>"
    return html

if __name__ == '__main__':
    app.run(debug=True, port=5001)
    try:
        # Generate slot conflicts
        from helpers.time_utils import generate_slot_conflicts
        slot_conflicts = generate_slot_conflicts(app.timetable)
        
        # Register routes with required parameters
        register_basic_routes(app, app.timetable)
        register_course_routes(app, app.all_courses, app.all_teachers)
        register_validation_routes(app, app.timetable, slot_conflicts)
        register_course_management_routes(app, app.timetable, slot_conflicts)
        register_optimization_routes(app, app.timetable, slot_conflicts)
        register_export_import_routes(app, app.timetable, app.all_teachers)
        
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
        return '<h1>404 - Page Not Found</h1><p>The requested resource was not found.</p>', 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        if request.is_json:
            return jsonify({
                'success': False,
                'message': 'Internal server error',
                'error_code': 500
            }), 500
        return '<h1>500 - Internal Server Error</h1><p>Something went wrong on the server.</p>', 500
    
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
    port = int(os.environ.get('FLASK_PORT', 5001))
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