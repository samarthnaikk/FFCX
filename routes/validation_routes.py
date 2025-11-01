# Validation and utility routes
from flask import jsonify, request
from helpers.time_utils import get_conflict_details


def register_validation_routes(app, timetable_template, slot_conflicts):
    """Register validation and utility routes"""
    
    @app.route('/api/validate-slots')
    def validate_slots():
        """API endpoint to validate current slot selection for conflicts"""
        enrolled_slots = set()
        conflicts = []
        
        # Collect all enrolled slots
        for day_schedule in timetable_template.values():
            for slot in day_schedule:
                if slot['course'] and slot['slot']:
                    enrolled_slots.add(slot['slot'])
        
        # Check for conflicts
        for slot in enrolled_slots:
            if slot in slot_conflicts:
                conflicting_slots = slot_conflicts[slot]
                for conflict in conflicting_slots:
                    if conflict in enrolled_slots:
                        conflicts.append({
                            "slot1": slot,
                            "slot2": conflict,
                            "message": f"Slot {slot} conflicts with {conflict}"
                        })
        
        return jsonify({
            "enrolled_slots": list(enrolled_slots),
            "conflicts": conflicts,
            "is_valid": len(conflicts) == 0
        })

    @app.route('/api/slot-info')
    def get_slot_info():
        """API endpoint to get complete slot information and availability"""
        slot_info = {}
        
        for day, day_schedule in timetable_template.items():
            slot_info[day] = []
            for time_slot in day_schedule:
                slot_data = {
                    "time": time_slot["time"],
                    "available_slots": time_slot["available_slots"],
                    "selected_slot": time_slot["slot"] if time_slot["course"] else "",
                    "course": time_slot["course"],
                    "course_name": time_slot["name"],
                    "faculty": time_slot["faculty"],
                    "venue": time_slot["venue"],
                    "is_occupied": bool(time_slot["course"])
                }
                slot_info[day].append(slot_data)
        
        return jsonify(slot_info)

    @app.route('/api/debug-conflicts')
    def debug_conflicts():
        """Debug endpoint to see all generated conflicts and test specific cases"""
        # Test the specific case mentioned by user
        test_cases = {
            'L10_vs_E1': {
                'L10_time': None,
                'E1_time': None,
                'should_conflict': True,
                'actual_conflict': 'E1' in slot_conflicts.get('L10', [])
            }
        }
        
        # Get actual times for test slots
        for day, schedule in timetable_template.items():
            for slot_info in schedule:
                available_slots = slot_info['available_slots'].split('/')
                if 'L10' in available_slots:
                    test_cases['L10_vs_E1']['L10_time'] = slot_info['lab_time']
                if 'E1' in available_slots:
                    test_cases['L10_vs_E1']['E1_time'] = slot_info['theory_time']
        
        return jsonify({
            'total_conflicts': len(slot_conflicts),
            'test_cases': test_cases,
            'sample_conflicts': {k: v for k, v in list(slot_conflicts.items())[:5]},
            'L10_conflicts': slot_conflicts.get('L10', []),
            'E1_conflicts': slot_conflicts.get('E1', [])
        })