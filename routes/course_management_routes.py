# Course management routes (add/remove courses)
from flask import jsonify, request
from helpers.time_utils import get_conflict_details


def register_course_management_routes(app, timetable_template, slot_conflicts):
    """Register course management routes for adding and removing courses"""
    
    @app.route('/api/add-course', methods=['POST'])
    def add_course():
        """API endpoint to add a course to multiple slots (e.g., A1+B1 for theory+lab)"""
        try:
            data = request.get_json()
            subject_name = data.get('subject_name')
            slot_input = data.get('slot', '').strip()
            faculty = data.get('faculty')
            venue = data.get('venue')
            
            if not all([subject_name, slot_input, faculty, venue]):
                return jsonify({'success': False, 'message': 'All fields are required'}), 400
            
            # Parse multiple slots separated by '+'
            requested_slots = [s.strip().upper() for s in slot_input.split('+') if s.strip()]
            
            if not requested_slots:
                return jsonify({'success': False, 'message': 'Invalid slot format. Use format like A1 or A1+B1'}), 400
            
            # Get currently enrolled slots
            currently_enrolled_slots = set()
            for day_schedule in timetable_template.values():
                for time_slot in day_schedule:
                    if time_slot['course'] and time_slot['slot']:
                        currently_enrolled_slots.add(time_slot['slot'])
            
            # Check for conflicts with each requested slot
            for slot in requested_slots:
                # Check if requested slot conflicts with enrolled slots
                if slot in slot_conflicts:
                    conflicting_slots = slot_conflicts[slot]
                    for conflict_slot in conflicting_slots:
                        if conflict_slot in currently_enrolled_slots:
                            # Get detailed conflict information
                            conflict_details = get_conflict_details(slot, conflict_slot, timetable_template)
                            if conflict_details:
                                conflict_info = conflict_details[0]  # Take the first conflict
                                return jsonify({
                                    'success': False, 
                                    'message': f'Cannot add slot {slot} because it conflicts with already enrolled slot {conflict_slot} on {conflict_info["day"]} ({slot} {conflict_info["slot1_type"]}: {conflict_info["slot1_time"]} overlaps with {conflict_slot} {conflict_info["slot2_type"]}: {conflict_info["slot2_time"]}).'
                                }), 400
                
                # Check if enrolled slots conflict with this new slot
                for enrolled_slot in currently_enrolled_slots:
                    if enrolled_slot in slot_conflicts and slot in slot_conflicts[enrolled_slot]:
                        # Get detailed conflict information
                        conflict_details = get_conflict_details(enrolled_slot, slot, timetable_template)
                        if conflict_details:
                            conflict_info = conflict_details[0]  # Take the first conflict
                            return jsonify({
                                'success': False, 
                                'message': f'Cannot add slot {slot} because enrolled slot {enrolled_slot} conflicts with it on {conflict_info["day"]} ({enrolled_slot} {conflict_info["slot1_type"]}: {conflict_info["slot1_time"]} overlaps with {slot} {conflict_info["slot2_type"]}: {conflict_info["slot2_time"]}).'
                            }), 400
            
            # Check availability for all requested slots
            all_occupied_slots = []
            all_available_slots = []
            
            for slot in requested_slots:
                slot_occupied = []
                slot_available = []
                
                for day in timetable_template:
                    for time_index, time_slot in enumerate(timetable_template[day]):
                        available_options = time_slot['available_slots'].split('/')
                        
                        # Check if the requested slot is available in this time period
                        if slot in available_options:
                            if time_slot['course']:
                                slot_occupied.append(f"{slot} on {day} at {time_slot['time']}")
                            else:
                                slot_available.append((day, time_index, time_slot, slot))
                
                if slot_occupied:
                    all_occupied_slots.extend(slot_occupied)
                
                if not slot_available:
                    return jsonify({
                        'success': False, 
                        'message': f'Slot {slot} is not available in any time period'
                    }), 400
                
                all_available_slots.extend(slot_available)
            
            # If any slot instance is occupied, reject the entire request
            if all_occupied_slots:
                return jsonify({
                    'success': False, 
                    'message': f'Cannot add course. The following slots are already occupied: {", ".join(all_occupied_slots)}. Please choose different slots.'
                }), 400
            
            # Create a unique course identifier that includes all slots
            course_id = f"{subject_name}_{'+'.join(requested_slots)}"
            
            # Get course metadata from the form data
            course_code = data.get('course_code', '').strip()
            course_type = data.get('course_type', '').strip()
            credits = data.get('credits', 0)
            
            # Convert credits to float and validate
            try:
                credits = float(credits) if credits else 0
                # Validate credits range (typical university courses: 0.5 to 10 credits)
                if credits < 0 or credits > 10:
                    return jsonify({
                        'success': False,
                        'message': f'Invalid credits value: {credits}. Must be between 0 and 10.'
                    }), 400
            except (ValueError, TypeError):
                return jsonify({
                    'success': False,
                    'message': f'Invalid credits format: {credits}. Must be a number.'
                }), 400
            
            # Fill all available instances of all requested slots
            filled_slots = []
            for day, time_index, time_slot, slot in all_available_slots:
                timetable_template[day][time_index].update({
                    'course': course_id,  # Unique identifier for this multi-slot course
                    'name': subject_name,
                    'faculty': faculty,
                    'venue': venue,
                    'slot': slot,  # Individual slot for this time period
                    'course_code': course_code,  # Store actual course code
                    'course_type': course_type,  # Store course type
                    'credits': credits  # Store credits
                })
                filled_slots.append(f"{slot} on {day} at {time_slot['time']}")
            
            return jsonify({
                'success': True, 
                'message': f'Course "{subject_name}" added successfully to slots {"+".join(requested_slots)}: {", ".join(filled_slots)}',
                'filled_slots': filled_slots,
                'course_slots': requested_slots
            })
                
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    @app.route('/api/remove-course', methods=['POST'])
    def remove_course():
        """API endpoint to remove all instances of a course from the timetable"""
        try:
            data = request.get_json()
            day = data.get('day')
            time_index = data.get('time_index')
            
            if day not in timetable_template or not (0 <= time_index < len(timetable_template[day])):
                return jsonify({'success': False, 'message': 'Invalid day or time index'}), 400
            
            # Get the course to remove
            target_slot = timetable_template[day][time_index]
            if not target_slot['course']:
                return jsonify({'success': False, 'message': 'No course found at this slot'}), 400
            
            course_id = target_slot['course']  # This now includes the unique identifier
            course_name = target_slot['name']
            
            # Find and remove ALL instances of this course across the entire timetable
            removed_slots = []
            for d in timetable_template:
                for t_index, time_slot in enumerate(timetable_template[d]):
                    if time_slot['course'] == course_id:
                        # Store info about removed slot
                        removed_slots.append(f"{time_slot['slot']} on {d} at {time_slot['time']}")
                        
                        # Clear the slot
                        time_slot.update({
                            'course': '',
                            'name': '',
                            'faculty': '',
                            'venue': '',
                            'slot': '',
                            'course_code': '',
                            'course_type': '',
                            'credits': 0
                        })
            
            return jsonify({
                'success': True, 
                'message': f'Course "{course_name}" removed successfully from {len(removed_slots)} slot(s): {", ".join(removed_slots)}',
                'removed_slots': removed_slots
            })
                
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500