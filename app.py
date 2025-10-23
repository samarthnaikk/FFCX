from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# VIT FFCS Timetable Data based on actual slot structure
SAMPLE_TIMETABLE = {
    "Monday": [
        {"time": "08:00-08:50", "course": "CSE2001", "name": "Computer Programming", "faculty": "Dr. Smith", "venue": "SJT101", "slot": "A1", "available_slots": "A1/L1"},
        {"time": "09:00-09:50", "course": "CSE2004", "name": "Data Structures", "faculty": "Dr. Wilson", "venue": "SJT102", "slot": "F1", "available_slots": "F1/L2"},
        {"time": "10:00-10:50", "course": "PHY2006", "name": "Physics", "faculty": "Dr. Taylor", "venue": "AB1-202", "slot": "D1", "available_slots": "D1/L3"},
        {"time": "11:00-11:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TB1/L4"},
        {"time": "12:00-12:50", "course": "MAT2001", "name": "Calculus", "faculty": "Prof. Johnson", "venue": "AB2-101", "slot": "TG1", "available_slots": "TG1/L5"},
        {"time": "14:00-14:50", "course": "CSE2048", "name": "Programming Lab", "faculty": "Dr. Smith", "venue": "SJT-Lab1", "slot": "L31", "available_slots": "A2/L31"},
        {"time": "15:00-15:50", "course": "ENG1901", "name": "Technical English", "faculty": "Ms. Davis", "venue": "MB-205", "slot": "F2", "available_slots": "F2/L32"},
        {"time": "16:00-16:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "D2/L33"},
        {"time": "17:00-17:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TB2/L34"},
        {"time": "18:00-18:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TG2/L35"}
    ],
    "Tuesday": [
        {"time": "08:00-08:50", "course": "PHY2006", "name": "Physics", "faculty": "Dr. Taylor", "venue": "AB1-202", "slot": "B1", "available_slots": "B1/L7"},
        {"time": "09:00-09:50", "course": "CSE2004", "name": "Data Structures", "faculty": "Dr. Wilson", "venue": "SJT102", "slot": "G1", "available_slots": "G1/L8"},
        {"time": "10:00-10:50", "course": "MAT2001", "name": "Calculus", "faculty": "Prof. Johnson", "venue": "AB2-101", "slot": "E1", "available_slots": "E1/L9"},
        {"time": "11:00-11:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TC1/L10"},
        {"time": "12:00-12:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TAA1/L11"},
        {"time": "14:00-14:50", "course": "CSE2001", "name": "Computer Programming", "faculty": "Dr. Smith", "venue": "SJT101", "slot": "B2", "available_slots": "B2/L37"},
        {"time": "15:00-15:50", "course": "PHY2048", "name": "Physics Lab", "faculty": "Dr. Brown", "venue": "PHY-Lab1", "slot": "L38", "available_slots": "G2/L38"},
        {"time": "16:00-16:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "E2/L39"},
        {"time": "17:00-17:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TC2/L40"},
        {"time": "18:00-18:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TAA2/L41"}
    ],
    "Wednesday": [
        {"time": "08:00-08:50", "course": "MAT2001", "name": "Calculus", "faculty": "Prof. Johnson", "venue": "AB2-101", "slot": "C1", "available_slots": "C1/L13"},
        {"time": "09:00-09:50", "course": "CSE2001", "name": "Computer Programming", "faculty": "Dr. Smith", "venue": "SJT101", "slot": "A1", "available_slots": "A1/L14"},
        {"time": "10:00-10:50", "course": "CSE2004", "name": "Data Structures", "faculty": "Dr. Wilson", "venue": "SJT102", "slot": "F1", "available_slots": "F1/L15"},
        {"time": "11:00-11:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "V1/L16"},
        {"time": "12:00-12:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "V2/L17"},
        {"time": "14:00-14:50", "course": "ENG1901", "name": "Technical English", "faculty": "Ms. Davis", "venue": "MB-205", "slot": "C2", "available_slots": "C2/L43"},
        {"time": "15:00-15:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "A2/L44"},
        {"time": "16:00-16:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "F2/L45"},
        {"time": "17:00-17:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TD2/L46"},
        {"time": "18:00-18:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TBB2/L47"}
    ],
    "Thursday": [
        {"time": "08:00-08:50", "course": "PHY2006", "name": "Physics", "faculty": "Dr. Taylor", "venue": "AB1-202", "slot": "D1", "available_slots": "D1/L19"},
        {"time": "09:00-09:50", "course": "PHY2006", "name": "Physics", "faculty": "Dr. Taylor", "venue": "AB1-202", "slot": "B1", "available_slots": "B1/L20"},
        {"time": "10:00-10:50", "course": "CSE2004", "name": "Data Structures", "faculty": "Dr. Wilson", "venue": "SJT102", "slot": "G1", "available_slots": "G1/L21"},
        {"time": "11:00-11:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TE1/L22"},
        {"time": "12:00-12:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TCC1/L23"},
        {"time": "14:00-14:50", "course": "MAT2001", "name": "Calculus", "faculty": "Prof. Johnson", "venue": "AB2-101", "slot": "D2", "available_slots": "D2/L49"},
        {"time": "15:00-15:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "B2/L50"},
        {"time": "16:00-16:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "G2/L51"},
        {"time": "17:00-17:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TE2/L52"},
        {"time": "18:00-18:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TCC2/L53"}
    ],
    "Friday": [
        {"time": "08:00-08:50", "course": "MAT2001", "name": "Calculus", "faculty": "Prof. Johnson", "venue": "AB2-101", "slot": "E1", "available_slots": "E1/L25"},
        {"time": "09:00-09:50", "course": "ENG1901", "name": "Technical English", "faculty": "Ms. Davis", "venue": "MB-205", "slot": "C1", "available_slots": "C1/L26"},
        {"time": "10:00-10:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TA1/L27"},
        {"time": "11:00-11:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TF1/L28"},
        {"time": "12:00-12:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TD1/L29"},
        {"time": "14:00-14:50", "course": "CSE2048", "name": "Programming Lab", "faculty": "Dr. Smith", "venue": "SJT-Lab1", "slot": "L55", "available_slots": "E2/L55"},
        {"time": "15:00-15:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "C2/L56"},
        {"time": "16:00-16:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TA2/L57"},
        {"time": "17:00-17:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TF2/L58"},
        {"time": "18:00-18:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": "", "available_slots": "TDD2/L59"}
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

# VIT FFCS Slot conflict rules - if you take one slot, you cannot take the conflicting slot
SLOT_CONFLICTS = {
    # Monday conflicts
    "A1": ["L1"], "L1": ["A1"],
    "F1": ["L2"], "L2": ["F1"],
    "D1": ["L3"], "L3": ["D1"],
    "TB1": ["L4"], "L4": ["TB1"],
    "TG1": ["L5"], "L5": ["TG1"],
    "A2": ["L31"], "L31": ["A2"],
    "F2": ["L32"], "L32": ["F2"],
    "D2": ["L33"], "L33": ["D2"],
    "TB2": ["L34"], "L34": ["TB2"],
    "TG2": ["L35"], "L35": ["TG2"],
    
    # Tuesday conflicts
    "B1": ["L7"], "L7": ["B1"],
    "G1": ["L8"], "L8": ["G1"],
    "E1": ["L9"], "L9": ["E1"],
    "TC1": ["L10"], "L10": ["TC1"],
    "TAA1": ["L11"], "L11": ["TAA1"],
    "B2": ["L37"], "L37": ["B2"],
    "G2": ["L38"], "L38": ["G2"],
    "E2": ["L39"], "L39": ["E2"],
    "TC2": ["L40"], "L40": ["TC2"],
    "TAA2": ["L41"], "L41": ["TAA2"],
    
    # Wednesday conflicts
    "C1": ["L13"], "L13": ["C1"],
    "A1": ["L14"], "L14": ["A1"],
    "F1": ["L15"], "L15": ["F1"],
    "V1": ["L16"], "L16": ["V1"],
    "V2": ["L17"], "L17": ["V2"],
    "C2": ["L43"], "L43": ["C2"],
    "A2": ["L44"], "L44": ["A2"],
    "F2": ["L45"], "L45": ["F2"],
    "TD2": ["L46"], "L46": ["TD2"],
    "TBB2": ["L47"], "L47": ["TBB2"],
    
    # Thursday conflicts
    "D1": ["L19"], "L19": ["D1"],
    "B1": ["L20"], "L20": ["B1"],
    "G1": ["L21"], "L21": ["G1"],
    "TE1": ["L22"], "L22": ["TE1"],
    "TCC1": ["L23"], "L23": ["TCC1"],
    "D2": ["L49"], "L49": ["D2"],
    "B2": ["L50"], "L50": ["B2"],
    "G2": ["L51"], "L51": ["G2"],
    "TE2": ["L52"], "L52": ["TE2"],
    "TCC2": ["L53"], "L53": ["TCC2"],
    
    # Friday conflicts
    "E1": ["L25"], "L25": ["E1"],
    "C1": ["L26"], "L26": ["C1"],
    "TA1": ["L27"], "L27": ["TA1"],
    "TF1": ["L28"], "L28": ["TF1"],
    "TD1": ["L29"], "L29": ["TD1"],
    "E2": ["L55"], "L55": ["E2"],
    "C2": ["L56"], "L56": ["C2"],
    "TA2": ["L57"], "L57": ["TA2"],
    "TF2": ["L58"], "L58": ["TF2"],
    "TDD2": ["L59"], "L59": ["TDD2"]
}

@app.route('/')
def index():
    """Homepage with Vue.js timetable"""
    return render_template('index.html')

@app.route('/api/timetable')
def get_timetable():
    """API endpoint to get timetable data"""
    return jsonify(SAMPLE_TIMETABLE)

@app.route('/api/timetable/<day>')
def get_day_timetable(day):
    """API endpoint to get timetable for a specific day"""
    day_schedule = SAMPLE_TIMETABLE.get(day.capitalize(), [])
    return jsonify(day_schedule)

@app.route('/api/courses')
def get_courses():
    """API endpoint to get course information with timetable data"""
    courses = []
    enrolled_courses = set()
    enrolled_slots = set()
    
    # Collect all enrolled courses and slots from timetable
    for day_schedule in SAMPLE_TIMETABLE.values():
        for slot in day_schedule:
            if slot['course']:
                enrolled_courses.add(slot['course'])
                if slot['slot']:
                    enrolled_slots.add(slot['slot'])
    
    # Build course list with details
    for course_code in enrolled_courses:
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
            
            # Collect slots and faculty info for this course
            for day, day_schedule in SAMPLE_TIMETABLE.items():
                for slot in day_schedule:
                    if slot['course'] == course_code:
                        course_data["slots"].append(f"{slot['slot']} ({day[:3]})")
                        course_data["available_slots"].append(f"{slot['available_slots']} ({day[:3]})")
                        if not course_data["faculty"]:
                            course_data["faculty"] = slot['faculty']
            
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
    for day_schedule in SAMPLE_TIMETABLE.values():
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
    
    for day, day_schedule in SAMPLE_TIMETABLE.items():
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)