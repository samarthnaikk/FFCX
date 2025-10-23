from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

# Empty VIT FFCS Timetable Template - users can add/remove courses
TIMETABLE_TEMPLATE = {
    "Monday": [
        {"time": "08:00-08:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "A1"},
        {"time": "08:00-09:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L1"},
        {"time": "08:51-10:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L2"},
        {"time": "09:00-09:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "F1"},
        {"time": "09:51-11:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L3"},
        {"time": "10:00-10:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "D1"},
        {"time": "10:41-12:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L4"},
        {"time": "11:00-11:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TB1"},
        {"time": "11:40-13:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L5"},
        {"time": "12:00-12:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TG1"},
        {"time": "12:31-14:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L6"},
        {"time": "14:00-14:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "A2"},
        {"time": "14:00-15:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L31"},
        {"time": "14:51-16:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L32"},
        {"time": "15:00-15:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "F2"},
        {"time": "15:51-17:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L33"},
        {"time": "16:00-16:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "D2"},
        {"time": "16:41-18:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L34"},
        {"time": "17:00-17:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TB2"},
        {"time": "17:40-19:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L35"},
        {"time": "18:00-18:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TG2"},
        {"time": "18:31-20:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L36"}
    ],
    "Tuesday": [
        {"time": "08:00-08:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "B1"},
        {"time": "08:00-09:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L7"},
        {"time": "08:51-10:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L8"},
        {"time": "09:00-09:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "G1"},
        {"time": "09:51-11:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L9"},
        {"time": "10:00-10:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "E1"},
        {"time": "10:41-12:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L10"},
        {"time": "11:00-11:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TC1"},
        {"time": "11:40-13:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L11"},
        {"time": "12:00-12:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TAA1"},
        {"time": "12:31-14:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L12"},
        {"time": "14:00-14:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "B2"},
        {"time": "14:00-15:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L37"},
        {"time": "14:51-16:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L38"},
        {"time": "15:00-15:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "G2"},
        {"time": "15:51-17:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L39"},
        {"time": "16:00-16:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "E2"},
        {"time": "16:41-18:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L40"},
        {"time": "17:00-17:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TC2"},
        {"time": "17:40-19:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L41"},
        {"time": "18:00-18:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TAA2"},
        {"time": "18:31-20:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L42"}
    ],
    "Wednesday": [
        {"time": "08:00-08:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "C1"},
        {"time": "08:00-09:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L13"},
        {"time": "08:51-10:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L14"},
        {"time": "09:00-09:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "A1"},
        {"time": "09:51-11:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L15"},
        {"time": "10:00-10:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "F1"},
        {"time": "10:41-12:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L16"},
        {"time": "11:00-11:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "V1"},
        {"time": "11:40-13:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L17"},
        {"time": "12:00-12:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "V2"},
        {"time": "12:31-14:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L18"},
        {"time": "14:00-14:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "C2"},
        {"time": "14:00-15:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L43"},
        {"time": "14:51-16:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L44"},
        {"time": "15:00-15:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "A2"},
        {"time": "15:51-17:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L45"},
        {"time": "16:00-16:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "F2"},
        {"time": "16:41-18:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L46"},
        {"time": "17:00-17:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TD2"},
        {"time": "17:40-19:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L47"},
        {"time": "18:00-18:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TBB2"},
        {"time": "18:31-20:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L48"}
    ],
    "Thursday": [
        {"time": "08:00-08:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "D1"},
        {"time": "08:00-09:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L19"},
        {"time": "08:51-10:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L20"},
        {"time": "09:00-09:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "B1"},
        {"time": "09:51-11:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L21"},
        {"time": "10:00-10:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "G1"},
        {"time": "10:41-12:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L22"},
        {"time": "11:00-11:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TE1"},
        {"time": "11:40-13:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L23"},
        {"time": "12:00-12:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TCC1"},
        {"time": "12:31-14:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L24"},
        {"time": "14:00-14:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "D2"},
        {"time": "14:00-15:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L49"},
        {"time": "14:51-16:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L50"},
        {"time": "15:00-15:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "B2"},
        {"time": "15:51-17:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L51"},
        {"time": "16:00-16:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "G2"},
        {"time": "16:41-18:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L52"},
        {"time": "17:00-17:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TE2"},
        {"time": "17:40-19:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L53"},
        {"time": "18:00-18:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TCC2"},
        {"time": "18:31-20:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L54"}
    ],
    "Friday": [
        {"time": "08:00-08:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "E1"},
        {"time": "08:00-09:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L25"},
        {"time": "08:51-10:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L26"},
        {"time": "09:00-09:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "C1"},
        {"time": "09:51-11:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L27"},
        {"time": "10:00-10:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TA1"},
        {"time": "10:41-12:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L28"},
        {"time": "11:00-11:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TF1"},
        {"time": "11:40-13:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L29"},
        {"time": "12:00-12:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TD1"},
        {"time": "12:31-14:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L30"},
        {"time": "14:00-14:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "E2"},
        {"time": "14:00-15:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L55"},
        {"time": "14:51-16:40", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L56"},
        {"time": "15:00-15:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "C2"},
        {"time": "15:51-17:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L57"},
        {"time": "16:00-16:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TA2"},
        {"time": "16:41-18:30", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L58"},
        {"time": "17:00-17:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TF2"},
        {"time": "17:40-19:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L59"},
        {"time": "18:00-18:50", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "TDD2"},
        {"time": "18:31-20:20", "course": "", "name": "", "faculty": "", "venue": "", "slot": "", "available_slots": "L60"}
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
SLOT_CONFLICTS = {
    # Monday conflicts - Labs overlap with multiple theory slots
    "A1": ["L1"], "L1": ["A1"],  # L1: 08:00-09:40 (overlaps A1 + part of F1)
    "F1": ["L2"], "L2": ["F1"],  # L2: 08:51-10:40 (overlaps F1 + D1)
    "D1": ["L3"], "L3": ["D1"],  # L3: 09:51-11:30 (overlaps D1 + TB1)
    "TB1": ["L4"], "L4": ["TB1"], # L4: 10:41-12:30 (overlaps TB1 + TG1)
    "TG1": ["L5"], "L5": ["TG1"], # L5: 11:40-13:20 (overlaps TG1 + lunch)
    
    # Labs L1-L5 have extended conflicts due to their longer duration
    "L1": ["A1", "F1"], "F1": ["L1", "L2"], 
    "L2": ["F1", "D1"], "D1": ["L2", "L3"],
    "L3": ["D1", "TB1"], "TB1": ["L3", "L4"],
    "L4": ["TB1", "TG1"], "TG1": ["L4", "L5"],
    "L5": ["TG1"],
    
    "A2": ["L31"], "L31": ["A2"],
    "F2": ["L32"], "L32": ["F2"],
    "D2": ["L33"], "L33": ["D2"],
    "TB2": ["L34"], "L34": ["TB2"],
    "TG2": ["L35"], "L35": ["TG2"],
    
    # Extended afternoon lab conflicts
    "L31": ["A2", "F2"], "F2": ["L31", "L32"],
    "L32": ["F2", "D2"], "D2": ["L32", "L33"],
    "L33": ["D2", "TB2"], "TB2": ["L33", "L34"],
    "L34": ["TB2", "TG2"], "TG2": ["L34", "L35"],
    "L35": ["TG2"],
    
    # Tuesday conflicts with similar lab overlap patterns
    "B1": ["L7"], "L7": ["B1"],
    "G1": ["L8"], "L8": ["G1"],
    "E1": ["L9"], "L9": ["E1"],
    "TC1": ["L10"], "L10": ["TC1"],
    "TAA1": ["L11"], "L11": ["TAA1"],
    
    "L7": ["B1", "G1"], "G1": ["L7", "L8"],
    "L8": ["G1", "E1"], "E1": ["L8", "L9"],
    "L9": ["E1", "TC1"], "TC1": ["L9", "L10"],
    "L10": ["TC1", "TAA1"], "TAA1": ["L10", "L11"],
    "L11": ["TAA1"],
    
    "B2": ["L37"], "L37": ["B2"],
    "G2": ["L38"], "L38": ["G2"],
    "E2": ["L39"], "L39": ["E2"],
    "TC2": ["L40"], "L40": ["TC2"],
    "TAA2": ["L41"], "L41": ["TAA2"],
    
    "L37": ["B2", "G2"], "G2": ["L37", "L38"],
    "L38": ["G2", "E2"], "E2": ["L38", "L39"],
    "L39": ["E2", "TC2"], "TC2": ["L39", "L40"],
    "L40": ["TC2", "TAA2"], "TAA2": ["L40", "L41"],
    "L41": ["TAA2"],
    
    # Wednesday conflicts
    "C1": ["L13"], "L13": ["C1"],
    "A1": ["L14"], "L14": ["A1"],
    "F1": ["L15"], "L15": ["F1"],
    "V1": ["L16"], "L16": ["V1"],
    "V2": ["L17"], "L17": ["V2"],
    
    "L13": ["C1", "A1"], "A1": ["L13", "L14"],
    "L14": ["A1", "F1"], "F1": ["L14", "L15"],
    "L15": ["F1", "V1"], "V1": ["L15", "L16"],
    "L16": ["V1", "V2"], "V2": ["L16", "L17"],
    "L17": ["V2"],
    
    "C2": ["L43"], "L43": ["C2"],
    "A2": ["L44"], "L44": ["A2"],
    "F2": ["L45"], "L45": ["F2"],
    "TD2": ["L46"], "L46": ["TD2"],
    "TBB2": ["L47"], "L47": ["TBB2"],
    
    "L43": ["C2", "A2"], "A2": ["L43", "L44"],
    "L44": ["A2", "F2"], "F2": ["L44", "L45"],
    "L45": ["F2", "TD2"], "TD2": ["L45", "L46"],
    "L46": ["TD2", "TBB2"], "TBB2": ["L46", "L47"],
    "L47": ["TBB2"],
    
    # Thursday conflicts
    "D1": ["L19"], "L19": ["D1"],
    "B1": ["L20"], "L20": ["B1"],
    "G1": ["L21"], "L21": ["G1"],
    "TE1": ["L22"], "L22": ["TE1"],
    "TCC1": ["L23"], "L23": ["TCC1"],
    
    "L19": ["D1", "B1"], "B1": ["L19", "L20"],
    "L20": ["B1", "G1"], "G1": ["L20", "L21"],
    "L21": ["G1", "TE1"], "TE1": ["L21", "L22"],
    "L22": ["TE1", "TCC1"], "TCC1": ["L22", "L23"],
    "L23": ["TCC1"],
    
    "D2": ["L49"], "L49": ["D2"],
    "B2": ["L50"], "L50": ["B2"],
    "G2": ["L51"], "L51": ["G2"],
    "TE2": ["L52"], "L52": ["TE2"],
    "TCC2": ["L53"], "L53": ["TCC2"],
    
    "L49": ["D2", "B2"], "B2": ["L49", "L50"],
    "L50": ["B2", "G2"], "G2": ["L50", "L51"],
    "L51": ["G2", "TE2"], "TE2": ["L51", "L52"],
    "L52": ["TE2", "TCC2"], "TCC2": ["L52", "L53"],
    "L53": ["TCC2"],
    
    # Friday conflicts
    "E1": ["L25"], "L25": ["E1"],
    "C1": ["L26"], "L26": ["C1"],
    "TA1": ["L27"], "L27": ["TA1"],
    "TF1": ["L28"], "L28": ["TF1"],
    "TD1": ["L29"], "L29": ["TD1"],
    
    "L25": ["E1", "C1"], "C1": ["L25", "L26"],
    "L26": ["C1", "TA1"], "TA1": ["L26", "L27"],
    "L27": ["TA1", "TF1"], "TF1": ["L27", "L28"],
    "L28": ["TF1", "TD1"], "TD1": ["L28", "L29"],
    "L29": ["TD1"],
    
    "E2": ["L55"], "L55": ["E2"],
    "C2": ["L56"], "L56": ["C2"],
    "TA2": ["L57"], "L57": ["TA2"],
    "TF2": ["L58"], "L58": ["TF2"],
    "TDD2": ["L59"], "L59": ["TDD2"],
    
    "L55": ["E2", "C2"], 
    "L56": ["C2", "TA2"], 
    "L57": ["TA2", "TF2"], 
    "L58": ["TF2", "TDD2"], 
    "L59": ["TDD2"]
}

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
            for day, day_schedule in TIMETABLE_TEMPLATE.items():
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