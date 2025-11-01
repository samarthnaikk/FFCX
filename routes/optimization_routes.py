# Optimization and preference routes
from flask import jsonify, request
from features.validation import validate_priority_conflicts
from features.optimization import optimize_timetable_logic, move_course_logic


def register_optimization_routes(app, timetable_template, slot_conflicts):
    """Register optimization and preference-related routes"""
    
    @app.route('/api/optimize-timetable', methods=['POST'])
    def optimize_timetable():
        """Optimize timetable based on teacher preferences and priorities"""
        try:
            data = request.get_json()
            preferences = data.get('preferences', {})
            
            if not preferences:
                return jsonify({'success': False, 'message': 'No preferences provided'}), 400
            
            # Validate priority conflicts before optimization
            validation_errors = validate_priority_conflicts(preferences)
            if validation_errors:
                return jsonify({
                    'success': False, 
                    'message': f'Priority conflicts detected: {"; ".join(validation_errors)}'
                }), 400
            
            # Run optimization
            result = optimize_timetable_logic(preferences, timetable_template, slot_conflicts)
            return jsonify(result)
            
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    @app.route('/api/move-course', methods=['POST'])
    def move_course():
        """Move a course from one time slot to another"""
        try:
            data = request.get_json()
            from_day = data.get('from_day')
            from_index = int(data.get('from_index'))
            to_day = data.get('to_day')
            to_index = int(data.get('to_index'))
            course_data = data.get('course')
            
            success, message = move_course_logic(
                from_day, from_index, to_day, to_index, 
                course_data, timetable_template, slot_conflicts
            )
            
            return jsonify({
                'success': success, 
                'message': message
            })
            
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500