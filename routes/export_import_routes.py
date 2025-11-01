# Export/Import and teacher data routes
from flask import jsonify, request
import json
import base64
import zlib


def register_export_import_routes(app, timetable_template, teachers_by_course):
    """Register export/import and teacher data routes"""
    
    @app.route('/api/all-teachers')
    def get_all_teachers():
        """API endpoint to get all teacher data organized by course"""
        return jsonify(teachers_by_course)

    @app.route('/api/debug-teachers')
    def debug_teachers():
        """Debug endpoint to see what courses have teacher data"""
        debug_info = {
            'total_courses': len(teachers_by_course),
            'courses': []
        }
        
        for course_name, course_data in list(teachers_by_course.items())[:10]:  # Show first 10
            debug_info['courses'].append({
                'name': course_name,
                'code': course_data.get('course_code', ''),
                'teacher_count': len(course_data.get('teachers', []))
            })
        
        return jsonify(debug_info)

    @app.route('/api/export-timetable')
    def export_timetable():
        """Generate a compact shareable code for the current timetable"""
        try:
            # Extract unique courses with their slot combinations
            courses = {}
            
            for day, schedule in timetable_template.items():
                for slot in schedule:
                    if slot['course']:  # Only include occupied slots
                        course_id = slot['course']
                        
                        # If this is the first time we see this course, store its metadata
                        if course_id not in courses:
                            courses[course_id] = {
                                'n': slot['name'],  # name
                                'c': slot.get('course_code', ''),  # course_code
                                't': slot.get('course_type', ''),  # type
                                'r': slot.get('credits', 0),  # credits
                                'f': slot['faculty'],  # faculty
                                'v': slot['venue'],  # venue
                                's': []  # slots array
                            }
                        
                        # Add this slot if not already present
                        if slot['slot'] not in courses[course_id]['s']:
                            courses[course_id]['s'].append(slot['slot'])
            
            # Convert to compact format: just the courses with their slots
            compact_data = list(courses.values())
            
            # Convert to JSON and compress with maximum compression
            json_data = json.dumps(compact_data, separators=(',', ':'))
            compressed_data = zlib.compress(json_data.encode('utf-8'), level=9)
            encoded_data = base64.b64encode(compressed_data).decode('utf-8')
            
            # Add version prefix for compact format
            timetable_code = f"FFCX_V2_{encoded_data}"
            
            return jsonify({
                'success': True,
                'code': timetable_code,
                'courses_count': len(courses),
                'total_slots': sum(len(course['s']) for course in courses.values()),
                'code_length': len(timetable_code),
                'message': 'Compact timetable code generated successfully'
            })
            
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error generating code: {str(e)}'}), 500

    @app.route('/api/import-timetable', methods=['POST'])
    def import_timetable():
        """Load timetable from a shareable code (supports both V1 and V2 formats)"""
        try:
            data = request.get_json()
            timetable_code = data.get('code', '').strip()
            
            if not timetable_code:
                return jsonify({'success': False, 'message': 'Please provide a timetable code'}), 400
            
            # Determine version and extract data
            if timetable_code.startswith('FFCX_V2_'):
                # New compact format
                encoded_data = timetable_code[8:]  # Remove "FFCX_V2_" prefix
                return import_v2_format(encoded_data, timetable_template)
            elif timetable_code.startswith('FFCX_V1_'):
                # Legacy format
                encoded_data = timetable_code[8:]  # Remove "FFCX_V1_" prefix
                return import_v1_format(encoded_data, timetable_template)
            else:
                return jsonify({'success': False, 'message': 'Invalid or unsupported timetable code format'}), 400
            
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error loading timetable: {str(e)}'}), 500


def import_v2_format(encoded_data, timetable_template):
    """Import compact V2 format - reconstructs timetable from course+slots data"""
    try:
        # Decode and decompress
        compressed_data = base64.b64decode(encoded_data.encode('utf-8'))
        json_data = zlib.decompress(compressed_data).decode('utf-8')
        courses_data = json.loads(json_data)
        
        # Clear current timetable
        for day in timetable_template:
            for slot_index in range(len(timetable_template[day])):
                timetable_template[day][slot_index].update({
                    'course': '',
                    'name': '',
                    'faculty': '',
                    'venue': '',
                    'slot': '',
                    'course_code': '',
                    'course_type': '',
                    'credits': 0
                })
        
        imported_courses = 0
        total_slots_filled = 0
        failed_assignments = []
        
        # Reconstruct each course
        for course_data in courses_data:
            course_name = course_data.get('n', 'Unknown Course')
            course_code = course_data.get('c', '')
            course_type = course_data.get('t', '')
            credits = course_data.get('r', 0)
            faculty = course_data.get('f', '')
            venue = course_data.get('v', '')
            slots = course_data.get('s', [])
            
            # Create unique course identifier
            course_id = f"{course_name}_{'+'.join(slots)}"
            
            # Find and fill matching slots
            course_filled = False
            slots_for_this_course = 0
            
            for slot in slots:
                slot_found = False
                for day in timetable_template:
                    for slot_index, time_slot in enumerate(timetable_template[day]):
                        available_options = time_slot['available_slots'].split('/')
                        
                        if slot in available_options and not time_slot['course']:
                            time_slot.update({
                                'course': course_id,
                                'name': course_name,
                                'faculty': faculty,
                                'venue': venue,
                                'slot': slot,
                                'course_code': course_code,
                                'course_type': course_type,
                                'credits': credits
                            })
                            slot_found = True
                            course_filled = True
                            slots_for_this_course += 1
                            total_slots_filled += 1
                            break
                    if slot_found:
                        break
                
                if not slot_found:
                    failed_assignments.append(f"{course_name} - slot {slot}")
            
            if course_filled:
                imported_courses += 1
        
        message = f'Successfully imported {imported_courses} courses with {total_slots_filled} total slots'
        if failed_assignments:
            message += f'. Failed to assign: {", ".join(failed_assignments)}'
        
        return jsonify({
            'success': True,
            'message': message,
            'imported_courses': imported_courses,
            'total_slots_filled': total_slots_filled,
            'failed_assignments': failed_assignments
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error importing V2 format: {str(e)}'}), 500


def import_v1_format(encoded_data, timetable_template):
    """Import legacy V1 format - direct timetable data"""
    try:
        # Decode and decompress
        compressed_data = base64.b64decode(encoded_data.encode('utf-8'))
        json_data = zlib.decompress(compressed_data).decode('utf-8')
        imported_timetable = json.loads(json_data)
        
        # Validate structure
        if not isinstance(imported_timetable, dict):
            return jsonify({'success': False, 'message': 'Invalid timetable format'}), 400
        
        imported_courses = 0
        
        # Load the imported timetable
        for day, day_schedule in imported_timetable.items():
            if day in timetable_template and isinstance(day_schedule, list):
                for i, slot_data in enumerate(day_schedule):
                    if i < len(timetable_template[day]) and isinstance(slot_data, dict):
                        # Only import if there's a course in this slot
                        if slot_data.get('course'):
                            timetable_template[day][i].update({
                                'course': slot_data.get('course', ''),
                                'name': slot_data.get('name', ''),
                                'faculty': slot_data.get('faculty', ''),
                                'venue': slot_data.get('venue', ''),
                                'slot': slot_data.get('slot', ''),
                                'course_code': slot_data.get('course_code', ''),
                                'course_type': slot_data.get('course_type', ''),
                                'credits': slot_data.get('credits', 0)
                            })
                            if not any(c['course'] == slot_data.get('course') for c in 
                                     [slot for day_sched in timetable_template.values() for slot in day_sched]):
                                imported_courses += 1
        
        return jsonify({
            'success': True,
            'message': f'Successfully imported timetable with {imported_courses} courses'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error importing V1 format: {str(e)}'}), 500