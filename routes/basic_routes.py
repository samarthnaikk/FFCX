# Basic timetable routes
from flask import jsonify, render_template


def register_basic_routes(app, timetable_template):
    """Register basic routes like index, timetable display"""
    
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/timetable')
    def get_timetable():
        return jsonify(timetable_template)

    @app.route('/api/timetable/<day>')
    def get_day_timetable(day):
        if day in timetable_template:
            return jsonify({day: timetable_template[day]})
        return jsonify({'error': 'Day not found'}), 404