from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Empty VIT FFCS Timetable Template - users can add/remove courses
TIMETABLE_TEMPLATE = {
    "Monday": [
        {"time": "08:00-08:50", "theory_time": "08:00-08:50", "lab_time": "08:00-08:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "A1/L1"},
        {"time": "09:00-09:50", "theory_time": "09:00-09:50", "lab_time": "08:51-09:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "F1/L2"},
        {"time": "10:00-10:50", "theory_time": "10:00-10:50", "lab_time": "09:51-10:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "D1/L3"},
        {"time": "11:00-11:50", "theory_time": "11:00-11:50", "lab_time": "10:41-11:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TB1/L4"},
        {"time": "12:00-12:50", "theory_time": "12:00-12:50", "lab_time": "11:40-12:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TG1/L5"},
        {"time": "13:00-13:50", "theory_time": "LUNCH", "lab_time": "12:31-13:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "-/L6"},
        {"time": "14:00-14:50", "theory_time": "14:00-14:50", "lab_time": "14:00-14:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "A2/L31"},
        {"time": "15:00-15:50", "theory_time": "15:00-15:50", "lab_time": "14:51-15:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "F2/L32"},
        {"time": "16:00-16:50", "theory_time": "16:00-16:50", "lab_time": "15:51-16:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "D2/L33"},
        {"time": "17:00-17:50", "theory_time": "17:00-17:50", "lab_time": "16:41-17:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TB2/L34"},
        {"time": "18:00-18:50", "theory_time": "18:00-18:50", "lab_time": "17:40-18:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TG2/L35"},
        {"time": "18:51-19:50", "theory_time": "18:51-19:50", "lab_time": "18:31-19:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L36/-"}
    ],
    "Tuesday": [
        {"time": "08:00-08:50", "theory_time": "08:00-08:50", "lab_time": "08:00-08:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "B1/L7"},
        {"time": "09:00-09:50", "theory_time": "09:00-09:50", "lab_time": "08:51-09:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "G1/L8"},
        {"time": "10:00-10:50", "theory_time": "10:00-10:50", "lab_time": "09:51-10:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "E1/L9"},
        {"time": "11:00-11:50", "theory_time": "11:00-11:50", "lab_time": "10:41-11:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TC1/L10"},
        {"time": "12:00-12:50", "theory_time": "12:00-12:50", "lab_time": "11:40-12:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TAA1/L11"},
        {"time": "13:00-13:50", "theory_time": "LUNCH", "lab_time": "12:31-13:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "-/L12"},
        {"time": "14:00-14:50", "theory_time": "14:00-14:50", "lab_time": "14:00-14:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "B2/L37"},
        {"time": "15:00-15:50", "theory_time": "15:00-15:50", "lab_time": "14:51-15:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "G2/L38"},
        {"time": "16:00-16:50", "theory_time": "16:00-16:50", "lab_time": "15:51-16:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "E2/L39"},
        {"time": "17:00-17:50", "theory_time": "17:00-17:50", "lab_time": "16:41-17:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TC2/L40"},
        {"time": "18:00-18:50", "theory_time": "18:00-18:50", "lab_time": "17:40-18:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TAA2/L41"},
        {"time": "18:51-19:50", "theory_time": "18:51-19:50", "lab_time": "18:31-19:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L42/-"}
    ],
    "Wednesday": [
        {"time": "08:00-08:50", "theory_time": "08:00-08:50", "lab_time": "08:00-08:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "C1/L13"},
        {"time": "09:00-09:50", "theory_time": "09:00-09:50", "lab_time": "08:51-09:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "A1/L14"},
        {"time": "10:00-10:50", "theory_time": "10:00-10:50", "lab_time": "09:51-10:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "F1/L15"},
        {"time": "11:00-11:50", "theory_time": "11:00-11:50", "lab_time": "10:41-11:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "V1/L16"},
        {"time": "12:00-12:50", "theory_time": "12:00-12:50", "lab_time": "11:40-12:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "V2/L17"},
        {"time": "13:00-13:50", "theory_time": "LUNCH", "lab_time": "12:31-13:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "-/L18"},
        {"time": "14:00-14:50", "theory_time": "14:00-14:50", "lab_time": "14:00-14:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "C2/L43"},
        {"time": "15:00-15:50", "theory_time": "15:00-15:50", "lab_time": "14:51-15:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "A2/L44"},
        {"time": "16:00-16:50", "theory_time": "16:00-16:50", "lab_time": "15:51-16:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "F2/L45"},
        {"time": "17:00-17:50", "theory_time": "17:00-17:50", "lab_time": "16:41-17:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TD2/L46"},
        {"time": "18:00-18:50", "theory_time": "18:00-18:50", "lab_time": "17:40-18:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TBB2/L47"},
        {"time": "18:51-19:50", "theory_time": "18:51-19:50", "lab_time": "18:31-19:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L48/-"}
    ],
    "Thursday": [
        {"time": "08:00-08:50", "theory_time": "08:00-08:50", "lab_time": "08:00-08:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "D1/L19"},
        {"time": "09:00-09:50", "theory_time": "09:00-09:50", "lab_time": "08:51-09:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "B1/L20"},
        {"time": "10:00-10:50", "theory_time": "10:00-10:50", "lab_time": "09:51-10:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "G1/L21"},
        {"time": "11:00-11:50", "theory_time": "11:00-11:50", "lab_time": "10:41-11:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TE1/L22"},
        {"time": "12:00-12:50", "theory_time": "12:00-12:50", "lab_time": "11:40-12:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TCC1/L23"},
        {"time": "13:00-13:50", "theory_time": "LUNCH", "lab_time": "12:31-13:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "-/L24"},
        {"time": "14:00-14:50", "theory_time": "14:00-14:50", "lab_time": "14:00-14:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "D2/L49"},
        {"time": "15:00-15:50", "theory_time": "15:00-15:50", "lab_time": "14:51-15:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "B2/L50"},
        {"time": "16:00-16:50", "theory_time": "16:00-16:50", "lab_time": "15:51-16:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "G2/L51"},
        {"time": "17:00-17:50", "theory_time": "17:00-17:50", "lab_time": "16:41-17:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TE2/L52"},
        {"time": "18:00-18:50", "theory_time": "18:00-18:50", "lab_time": "17:40-18:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TCC2/L53"},
        {"time": "18:51-19:50", "theory_time": "18:51-19:50", "lab_time": "18:31-19:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L54/-"}
    ],
    "Friday": [
        {"time": "08:00-08:50", "theory_time": "08:00-08:50", "lab_time": "08:00-08:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "E1/L25"},
        {"time": "09:00-09:50", "theory_time": "09:00-09:50", "lab_time": "08:51-09:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "C1/L26"},
        {"time": "10:00-10:50", "theory_time": "10:00-10:50", "lab_time": "09:51-10:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TA1/L27"},
        {"time": "11:00-11:50", "theory_time": "11:00-11:50", "lab_time": "10:41-11:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TF1/L28"},
        {"time": "12:00-12:50", "theory_time": "12:00-12:50", "lab_time": "11:40-12:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TD1/L29"},
        {"time": "13:00-13:50", "theory_time": "LUNCH", "lab_time": "12:31-13:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "-/L30"},
        {"time": "14:00-14:50", "theory_time": "14:00-14:50", "lab_time": "14:00-14:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "E2/L55"},
        {"time": "15:00-15:50", "theory_time": "15:00-15:50", "lab_time": "14:51-15:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "C2/L56"},
        {"time": "16:00-16:50", "theory_time": "16:00-16:50", "lab_time": "15:51-16:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TA2/L57"},
        {"time": "17:00-17:50", "theory_time": "17:00-17:50", "lab_time": "16:41-17:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TF2/L58"},
        {"time": "18:00-18:50", "theory_time": "18:00-18:50", "lab_time": "17:40-18:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TDD2/L59"},
        {"time": "18:51-19:50", "theory_time": "18:51-19:50", "lab_time": "18:31-19:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L60/-"}
    ]
}

# VIT Course information with credits
COURSE_INFO = {
    "CSE2001": {"name": "Computer Programming", "credits": 4, "type": "Theory + Lab"},
    "CSE2004": {"name": "Data Structures and Algorithms", "credits": 4, "type": "Theory + Lab"},
    "CSE2048": {"name": "Computer Programming Lab", "credits": 2, "type": "Lab"},
    "MAT2001": {"name": "Calculus for Engineers", "credits": 4, "type": "Theory"},
    "PHY2006": {"name": "Physics for Engineers", "credits": 3, "type": "Theory"},
    "PHY2048": {"name": "Physics Lab", "credits": 1, "type": "Lab"},
    "ENG1901": {"name": "Technical English", "credits": 3, "type": "Theory"}
}

# VIT FFCS Slot conflict rules - Labs have different timings and conflicts
# Lab sessions typically run for 1 hour 50 minutes (110 minutes) spanning multiple theory periods
def _parse_hhmm(t):
    """Parse a single HH:MM string to minutes since midnight. Returns int or None."""
    try:
        hour, minute = map(int, t.split(':'))
        return hour * 60 + minute
    except Exception:
        return None


def parse_time_range(range_str):
    """Parse a range like '08:00-08:50' into (start_min, end_min) or (None, None) for non-times."""
    if not range_str or range_str in ('LUNCH', '-', ''):
        return None, None
    parts = range_str.split('-')
    if len(parts) != 2:
        return None, None
    start = _parse_hhmm(parts[0].strip())
    end = _parse_hhmm(parts[1].strip())
    if start is None or end is None:
        return None, None
    return start, end


def range_overlap(r1, r2):
    """Return True if two (start,end) minute ranges overlap."""
    if r1[0] is None or r1[1] is None or r2[0] is None or r2[1] is None:
        return False
    return r1[0] < r2[1] and r2[0] < r1[1]


def generate_slot_conflicts():
    """Generate comprehensive slot conflicts based on actual time overlaps.

    This function collects all time ranges where a given slot appears (a slot may appear
    in multiple day/time entries). It then marks two slots as conflicting if any of their
    time ranges overlap.
    """
    from collections import defaultdict

    slot_ranges = defaultdict(list)  # slot -> list of (start,end)

    # Collect ranges for each slot across timetable
    for day, schedule in TIMETABLE_TEMPLATE.items():
        for slot_info in schedule:
            available_slots = [s.strip() for s in slot_info['available_slots'].split('/')]
            theory_range = parse_time_range(slot_info.get('theory_time', ''))
            lab_range = parse_time_range(slot_info.get('lab_time', ''))

            for s in available_slots:
                if not s or s == '-':
                    continue
                if s.startswith('L'):
                    if lab_range[0] is not None:
                        slot_ranges[s].append(lab_range)
                else:
                    if theory_range[0] is not None:
                        slot_ranges[s].append(theory_range)

    # Build conflict map
    conflicts = {s: [] for s in slot_ranges}

    slots = list(slot_ranges.keys())
    for i, s1 in enumerate(slots):
        for j, s2 in enumerate(slots):
            if s1 == s2:
                continue
            # If any range of s1 overlaps any range of s2, they conflict
            overlap_found = False
            for r1 in slot_ranges[s1]:
                for r2 in slot_ranges[s2]:
                    if range_overlap(r1, r2):
                        overlap_found = True
                        break
                if overlap_found:
                    break
            if overlap_found:
                conflicts[s1].append(s2)

    return conflicts


# Generate conflicts dynamically based on actual time overlaps
SLOT_CONFLICTS = generate_slot_conflicts()

@app.route('/')
def index():
    """Homepage with Vue.js timetable"""
    return render_template('index.html')

@app.route('/api/timetable')
def get_timetable():
    """API endpoint to get timetable data"""
    return jsonify(TIMETABLE_TEMPLATE)

@app.route('/api/timetable/<day>')
def get_day_timetable(day):
    """API endpoint to get timetable for a specific day"""
    day_schedule = TIMETABLE_TEMPLATE.get(day.capitalize(), [])
    return jsonify(day_schedule)

@app.route('/api/courses')
def get_courses():
    """API endpoint to get course information with timetable data"""
    courses = []
    enrolled_courses = set()
    enrolled_slots = set()
    
    # Collect all enrolled courses and slots from timetable
    for day_schedule in TIMETABLE_TEMPLATE.values():
        for slot in day_schedule:
            if slot['course']:
                enrolled_courses.add(slot['course'])
                if slot['slot']:
                    enrolled_slots.add(slot['slot'])
    
    # Build course list with details
    for course_code in enrolled_courses:
        # Handle both predefined courses and manually added courses
        if course_code in COURSE_INFO:
            course_data = {
                "course_code": course_code,
                "name": COURSE_INFO[course_code]["name"],
                "credits": COURSE_INFO[course_code]["credits"],
                "type": COURSE_INFO[course_code]["type"],
                "slots": [],
                "faculty": "",
                "venue": "",
                "available_slots": []
            }
        else:
            # For manually added courses, use the subject name and slot info from timetable
            course_data = {
                "course_code": course_code,
                "name": "",  # Will be filled from timetable data
                "credits": 0,  # Unknown for manually added courses
                "type": "Unknown",
                "slots": [],
                "faculty": "",
                "venue": "",
                "available_slots": []
            }
            
        # Collect slots and faculty info for this course
        for day, day_schedule in TIMETABLE_TEMPLATE.items():
            for slot in day_schedule:
                if slot['course'] == course_code:
                    course_data["slots"].append(f"{slot['slot']} ({day[:3]})")
                    course_data["available_slots"].append(f"{slot['available_slots']} ({day[:3]})")
                    if not course_data["faculty"]:
                        course_data["faculty"] = slot['faculty']
                    if not course_data["name"] and slot['name']:
                        course_data["name"] = slot['name']
                    if not course_data["venue"]:
                        course_data["venue"] = slot['venue']
        
        course_data["slots"] = ", ".join(course_data["slots"])
        course_data["available_slots"] = ", ".join(course_data["available_slots"])
        courses.append(course_data)
    
    return jsonify(courses)

@app.route('/api/validate-slots')
def validate_slots():
    """API endpoint to validate current slot selection for conflicts"""
    enrolled_slots = set()
    conflicts = []
    
    # Collect all enrolled slots
    for day_schedule in TIMETABLE_TEMPLATE.values():
        for slot in day_schedule:
            if slot['course'] and slot['slot']:
                enrolled_slots.add(slot['slot'])
    
    # Check for conflicts
    for slot in enrolled_slots:
        if slot in SLOT_CONFLICTS:
            conflicting_slots = SLOT_CONFLICTS[slot]
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
    
    for day, day_schedule in TIMETABLE_TEMPLATE.items():
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
            'actual_conflict': 'E1' in SLOT_CONFLICTS.get('L10', [])
        }
    }
    
    # Get actual times for test slots
    for day, schedule in TIMETABLE_TEMPLATE.items():
        for slot_info in schedule:
            available_slots = slot_info['available_slots'].split('/')
            if 'L10' in available_slots:
                test_cases['L10_vs_E1']['L10_time'] = slot_info['lab_time']
            if 'E1' in available_slots:
                test_cases['L10_vs_E1']['E1_time'] = slot_info['theory_time']
    
    return jsonify({
        'total_conflicts': len(SLOT_CONFLICTS),
        'test_cases': test_cases,
        'sample_conflicts': {k: v for k, v in list(SLOT_CONFLICTS.items())[:5]},
        'L10_conflicts': SLOT_CONFLICTS.get('L10', []),
        'E1_conflicts': SLOT_CONFLICTS.get('E1', [])
    })

@app.route('/api/add-course', methods=['POST'])
def add_course():
    """API endpoint to add a course to all instances of a specific slot"""
    try:
        data = request.get_json()
        subject_name = data.get('subject_name')
        slot = data.get('slot')
        faculty = data.get('faculty')
        venue = data.get('venue')
        
        if not all([subject_name, slot, faculty, venue]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        # Check for slot conflicts first
        currently_enrolled_slots = set()
        for day_schedule in TIMETABLE_TEMPLATE.values():
            for time_slot in day_schedule:
                if time_slot['course'] and time_slot['slot']:
                    currently_enrolled_slots.add(time_slot['slot'])
        
        # Check if the requested slot conflicts with any currently enrolled slots
        if slot in SLOT_CONFLICTS:
            conflicting_slots = SLOT_CONFLICTS[slot]
            for conflict_slot in conflicting_slots:
                if conflict_slot in currently_enrolled_slots:
                    return jsonify({
                        'success': False, 
                        'message': f'Cannot add slot {slot} because it conflicts with already enrolled slot {conflict_slot}. Lab sessions overlap with theory sessions.'
                    }), 400
        
        # Check if any currently enrolled slots would conflict with this new slot
        for enrolled_slot in currently_enrolled_slots:
            if enrolled_slot in SLOT_CONFLICTS and slot in SLOT_CONFLICTS[enrolled_slot]:
                return jsonify({
                    'success': False, 
                    'message': f'Cannot add slot {slot} because enrolled slot {enrolled_slot} conflicts with it. Lab sessions overlap with theory sessions.'
                }), 400
        
        # First, check if any instance of this slot is already occupied
        occupied_slots = []
        available_slots = []
        
        for day in TIMETABLE_TEMPLATE:
            for time_index, time_slot in enumerate(TIMETABLE_TEMPLATE[day]):
                available_options = time_slot['available_slots'].split('/')
                
                # Check if the requested slot is available in this time period
                if slot in available_options:
                    if time_slot['course']:
                        occupied_slots.append(f"{day} at {time_slot['time']}")
                    else:
                        available_slots.append((day, time_index, time_slot))
        
        # If any instance is occupied, reject the request
        if occupied_slots:
            return jsonify({
                'success': False, 
                'message': f'Slot {slot} is already occupied on: {", ".join(occupied_slots)}. Please choose a different slot.'
            }), 400
        
        # If no instances are occupied, check if slot exists at all
        if not available_slots:
            return jsonify({
                'success': False, 
                'message': f'Slot {slot} is not available in any time period'
            }), 400
        
        # Fill all available instances of this slot
        filled_slots = []
        for day, time_index, time_slot in available_slots:
            TIMETABLE_TEMPLATE[day][time_index].update({
                'course': slot,  # Using slot as course identifier
                'name': subject_name,
                'faculty': faculty,
                'venue': venue,
                'slot': slot
            })
            filled_slots.append(f"{day} at {time_slot['time']}")
        
        return jsonify({
            'success': True, 
            'message': f'Course "{subject_name}" added successfully to all {slot} slots: {", ".join(filled_slots)}',
            'filled_slots': filled_slots
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
        
        if day not in TIMETABLE_TEMPLATE or not (0 <= time_index < len(TIMETABLE_TEMPLATE[day])):
            return jsonify({'success': False, 'message': 'Invalid day or time index'}), 400
        
        # Get the course and slot to remove
        target_slot = TIMETABLE_TEMPLATE[day][time_index]
        if not target_slot['course']:
            return jsonify({'success': False, 'message': 'No course found at this slot'}), 400
        
        course_name = target_slot['name']
        slot_to_remove = target_slot['slot']
        
        # Remove all instances of this course/slot from the timetable
        removed_slots = []
        for day_key in TIMETABLE_TEMPLATE:
            for idx, time_slot in enumerate(TIMETABLE_TEMPLATE[day_key]):
                if (time_slot['course'] and time_slot['slot'] == slot_to_remove and 
                    time_slot['name'] == course_name):
                    TIMETABLE_TEMPLATE[day_key][idx].update({
                        'course': '',
                        'name': '',
                        'faculty': '',
                        'venue': '',
                        'slot': ''
                    })
                    removed_slots.append(f"{day_key} at {time_slot['time']}")
        
        if removed_slots:
            return jsonify({
                'success': True, 
                'message': f'Course "{course_name}" removed from all slots: {", ".join(removed_slots)}'
            })
        else:
            return jsonify({'success': False, 'message': 'No matching course instances found'}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/available-courses')
def get_available_courses():
    """API endpoint to get list of available courses"""
    available_courses = []
    for course_code, course_info in COURSE_INFO.items():
        available_courses.append({
            'code': course_code,
            'name': course_info['name'],
            'credits': course_info['credits'],
            'type': course_info['type']
        })
    return jsonify(available_courses)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)