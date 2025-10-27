from flask import Flask, render_template, jsonify, request
import json
import csv
import os
import base64
import zlib

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

def load_courses_from_csv():
    """Load courses from courses.csv file"""
    courses = []
    csv_path = os.path.join(os.path.dirname(__file__), 'courses.csv')
    
    if not os.path.exists(csv_path):
        return courses
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Skip empty rows or rows without course title
                if not row.get('Course Title', '').strip():
                    continue
                    
                course = {
                    'course_code': row.get('Course Code', '').strip(),
                    'title': row.get('Course Title', '').strip(),
                    'type': row.get('Course Type', '').strip(),
                    'credits': float(row.get('Credits', 0))
                }
                courses.append(course)
    except Exception as e:
        print(f"Error loading courses.csv: {e}")
    
    return courses

# Load courses at startup
AVAILABLE_COURSES = load_courses_from_csv()

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
    for course_id in enrolled_courses:
        # Get the first instance of this course to extract metadata
        first_instance = None
        for day_schedule in TIMETABLE_TEMPLATE.values():
            for slot in day_schedule:
                if slot['course'] == course_id:
                    first_instance = slot
                    break
            if first_instance:
                break
        
        if not first_instance:
            continue
            
        # Check if this is a predefined course by looking at the stored course_code
        stored_course_code = first_instance.get('course_code', '')
        if stored_course_code and stored_course_code in COURSE_INFO:
            # Use predefined course info but override with stored data if available
            course_data = {
                "course_code": stored_course_code,
                "name": first_instance.get('name', COURSE_INFO[stored_course_code]["name"]),
                "credits": first_instance.get('credits', COURSE_INFO[stored_course_code]["credits"]),
                "type": first_instance.get('course_type', COURSE_INFO[stored_course_code]["type"]),
                "slots": [],
                "faculty": "",
                "venue": "",
                "available_slots": []
            }
        else:
            # For manually added courses, use stored metadata
            course_data = {
                "course_code": stored_course_code or "N/A",
                "name": first_instance.get('name', 'Unknown Course'),
                "credits": first_instance.get('credits', 0),
                "type": first_instance.get('course_type', 'Unknown'),
                "slots": [],
                "faculty": "",
                "venue": "",
                "available_slots": []
            }
            
        # Collect slots and faculty info for this course
        for day, day_schedule in TIMETABLE_TEMPLATE.items():
            for slot in day_schedule:
                if slot['course'] == course_id:
                    course_data["slots"].append(f"{slot['slot']} ({day[:3]})")
                    course_data["available_slots"].append(f"{slot['available_slots']} ({day[:3]})")
                    if not course_data["faculty"]:
                        course_data["faculty"] = slot['faculty']
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
        for day_schedule in TIMETABLE_TEMPLATE.values():
            for time_slot in day_schedule:
                if time_slot['course'] and time_slot['slot']:
                    currently_enrolled_slots.add(time_slot['slot'])
        
        # Check for conflicts with each requested slot
        for slot in requested_slots:
            # Check if requested slot conflicts with enrolled slots
            if slot in SLOT_CONFLICTS:
                conflicting_slots = SLOT_CONFLICTS[slot]
                for conflict_slot in conflicting_slots:
                    if conflict_slot in currently_enrolled_slots:
                        return jsonify({
                            'success': False, 
                            'message': f'Cannot add slot {slot} because it conflicts with already enrolled slot {conflict_slot}. Lab sessions overlap with theory sessions.'
                        }), 400
            
            # Check if enrolled slots conflict with this new slot
            for enrolled_slot in currently_enrolled_slots:
                if enrolled_slot in SLOT_CONFLICTS and slot in SLOT_CONFLICTS[enrolled_slot]:
                    return jsonify({
                        'success': False, 
                        'message': f'Cannot add slot {slot} because enrolled slot {enrolled_slot} conflicts with it. Lab sessions overlap with theory sessions.'
                    }), 400
        
        # Check availability for all requested slots
        all_occupied_slots = []
        all_available_slots = []
        
        for slot in requested_slots:
            slot_occupied = []
            slot_available = []
            
            for day in TIMETABLE_TEMPLATE:
                for time_index, time_slot in enumerate(TIMETABLE_TEMPLATE[day]):
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
        
        # Convert credits to float if it's a string
        try:
            credits = float(credits) if credits else 0
        except (ValueError, TypeError):
            credits = 0
        
        # Fill all available instances of all requested slots
        filled_slots = []
        for day, time_index, time_slot, slot in all_available_slots:
            TIMETABLE_TEMPLATE[day][time_index].update({
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
        
        if day not in TIMETABLE_TEMPLATE or not (0 <= time_index < len(TIMETABLE_TEMPLATE[day])):
            return jsonify({'success': False, 'message': 'Invalid day or time index'}), 400
        
        # Get the course to remove
        target_slot = TIMETABLE_TEMPLATE[day][time_index]
        if not target_slot['course']:
            return jsonify({'success': False, 'message': 'No course found at this slot'}), 400
        
        course_id = target_slot['course']  # This now includes the unique identifier
        course_name = target_slot['name']
        
        # Remove ALL instances of this course (all slots) from the timetable
        removed_slots = []
        for day_key in TIMETABLE_TEMPLATE:
            for idx, time_slot in enumerate(TIMETABLE_TEMPLATE[day_key]):
                if time_slot['course'] == course_id:  # Match by course ID (which includes all slots)
                    removed_slots.append(f"{time_slot['slot']} on {day_key} at {time_slot['time']}")
                    TIMETABLE_TEMPLATE[day_key][idx].update({
                        'course': '',
                        'name': '',
                        'faculty': '',
                        'venue': '',
                        'slot': ''
                    })
        
        if removed_slots:
            return jsonify({
                'success': True, 
                'message': f'Course "{course_name}" removed from all its slots: {", ".join(removed_slots)}'
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

@app.route('/api/search-courses')
def search_courses():
    """API endpoint to search courses by name or code"""
    query = request.args.get('q', '').strip().lower()
    
    if not query:
        return jsonify([])
    
    results = []
    for course in AVAILABLE_COURSES:
        # Search in course title and course code
        if (query in course['title'].lower() or 
            query in course['course_code'].lower()):
            results.append(course)
    
    # Limit results to prevent too many options
    return jsonify(results[:20])

@app.route('/api/export-timetable')
def export_timetable():
    """Generate a compact shareable code for the current timetable"""
    try:
        # Extract unique courses with their slot combinations
        courses = {}
        
        for day, schedule in TIMETABLE_TEMPLATE.items():
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
            return import_v2_format(encoded_data)
        elif timetable_code.startswith('FFCX_V1_'):
            # Legacy format
            encoded_data = timetable_code[8:]  # Remove "FFCX_V1_" prefix
            return import_v1_format(encoded_data)
        else:
            return jsonify({'success': False, 'message': 'Invalid or unsupported timetable code format'}), 400
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error loading timetable: {str(e)}'}), 500

def import_v2_format(encoded_data):
    """Import compact V2 format - reconstructs timetable from course+slots data"""
    try:
        # Decode and decompress
        compressed_data = base64.b64decode(encoded_data.encode('utf-8'))
        json_data = zlib.decompress(compressed_data).decode('utf-8')
        courses_data = json.loads(json_data)
        
        # Clear current timetable
        for day in TIMETABLE_TEMPLATE:
            for slot_index in range(len(TIMETABLE_TEMPLATE[day])):
                TIMETABLE_TEMPLATE[day][slot_index].update({
                    'course': '',
                    'name': '',
                    'faculty': '',
                    'venue': '',
                    'slot': '',
                    'course_code': '',
                    'course_type': '',
                    'credits': 0
                })
        
        # Reconstruct timetable from compact course data
        loaded_courses = 0
        total_slots = 0
        
        for course in courses_data:
            # Extract course metadata (using short keys)
            course_name = course['n']
            course_code = course.get('c', '')
            course_type = course.get('t', '')
            credits = course.get('r', 0)
            faculty = course['f']
            venue = course['v']
            slots = course['s']
            
            # Create unique course identifier
            course_id = f"{course_name}_{'+'.join(slots)}"
            
            # Place this course in all timetable positions where its slots appear
            for slot_name in slots:
                for day in TIMETABLE_TEMPLATE:
                    for slot_index, time_slot in enumerate(TIMETABLE_TEMPLATE[day]):
                        available_options = time_slot['available_slots'].split('/')
                        
                        # If this slot appears in this time position, place the course there
                        if slot_name in available_options:
                            TIMETABLE_TEMPLATE[day][slot_index].update({
                                'course': course_id,
                                'name': course_name,
                                'course_code': course_code,
                                'course_type': course_type,
                                'credits': credits,
                                'slot': slot_name,
                                'faculty': faculty,
                                'venue': venue
                            })
                            total_slots += 1
            
            loaded_courses += 1
        
        return jsonify({
            'success': True,
            'message': f'Compact timetable loaded successfully! {loaded_courses} courses with {total_slots} time slots imported.',
            'courses_loaded': loaded_courses,
            'slots_filled': total_slots
        })
        
    except Exception as e:
        raise Exception(f'V2 format error: {str(e)}')

def import_v1_format(encoded_data):
    """Import legacy V1 format for backward compatibility"""
    try:
        # Decode and decompress
        compressed_data = base64.b64decode(encoded_data.encode('utf-8'))
        json_data = zlib.decompress(compressed_data).decode('utf-8')
        timetable_data = json.loads(json_data)
        
        # Clear current timetable
        for day in TIMETABLE_TEMPLATE:
            for slot_index in range(len(TIMETABLE_TEMPLATE[day])):
                TIMETABLE_TEMPLATE[day][slot_index].update({
                    'course': '',
                    'name': '',
                    'faculty': '',
                    'venue': '',
                    'slot': '',
                    'course_code': '',
                    'course_type': '',
                    'credits': 0
                })
        
        # Load courses from V1 format (day-by-day with slot indices)
        loaded_courses = 0
        for day, courses in timetable_data.items():
            if day in TIMETABLE_TEMPLATE:
                for course in courses:
                    slot_index = course['slot_index']
                    if 0 <= slot_index < len(TIMETABLE_TEMPLATE[day]):
                        course_id = f"{course['name']}_{course['slot']}"
                        
                        TIMETABLE_TEMPLATE[day][slot_index].update({
                            'course': course_id,
                            'name': course['name'],
                            'course_code': course.get('course_code', ''),
                            'course_type': course.get('course_type', ''),
                            'credits': course.get('credits', 0),
                            'slot': course['slot'],
                            'faculty': course['faculty'],
                            'venue': course['venue']
                        })
                        loaded_courses += 1
        
        return jsonify({
            'success': True,
            'message': f'Legacy timetable loaded successfully! {loaded_courses} courses imported.',
            'courses_loaded': loaded_courses
        })
        
    except Exception as e:
        raise Exception(f'V1 format error: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)