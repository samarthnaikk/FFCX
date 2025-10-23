from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Sample timetable data
SAMPLE_TIMETABLE = {
    "Monday": [
        {"time": "08:00-08:50", "course": "CSE2001", "name": "Computer Programming", "faculty": "Dr. Smith", "venue": "SJT101", "slot": "A1"},
        {"time": "09:00-09:50", "course": "MAT2001", "name": "Calculus", "faculty": "Prof. Johnson", "venue": "AB2-101", "slot": "B1"},
        {"time": "10:00-10:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": ""},
        {"time": "11:00-11:50", "course": "PHY2048", "name": "Physics Lab", "faculty": "Dr. Brown", "venue": "AB2-301", "slot": "D1"},
        {"time": "14:00-14:50", "course": "ENG1901", "name": "Technical English", "faculty": "Ms. Davis", "venue": "MB-205", "slot": "F1"},
        {"time": "15:00-15:50", "course": "CSE2004", "name": "Data Structures", "faculty": "Dr. Wilson", "venue": "SJT102", "slot": "G1"},
        {"time": "16:00-16:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": ""},
        {"time": "17:00-17:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": ""}
    ],
    "Tuesday": [
        {"time": "08:00-08:50", "course": "MAT2001", "name": "Calculus", "faculty": "Prof. Johnson", "venue": "AB2-101", "slot": "A2"},
        {"time": "09:00-09:50", "course": "CSE2004", "name": "Data Structures", "faculty": "Dr. Wilson", "venue": "SJT102", "slot": "B2"},
        {"time": "10:00-10:50", "course": "PHY2006", "name": "Physics", "faculty": "Dr. Taylor", "venue": "AB1-202", "slot": "C2"},
        {"time": "11:00-11:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": ""},
        {"time": "14:00-14:50", "course": "CSE2001", "name": "Computer Programming", "faculty": "Dr. Smith", "venue": "SJT101", "slot": "F2"},
        {"time": "15:00-15:50", "course": "ENG1901", "name": "Technical English", "faculty": "Ms. Davis", "venue": "MB-205", "slot": "G2"},
        {"time": "16:00-16:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": ""},
        {"time": "17:00-17:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": ""}
    ],
    "Wednesday": [
        {"time": "08:00-08:50", "course": "CSE2004", "name": "Data Structures", "faculty": "Dr. Wilson", "venue": "SJT102", "slot": "A3"},
        {"time": "09:00-09:50", "course": "PHY2006", "name": "Physics", "faculty": "Dr. Taylor", "venue": "AB1-202", "slot": "B3"},
        {"time": "10:00-10:50", "course": "MAT2001", "name": "Calculus", "faculty": "Prof. Johnson", "venue": "AB2-101", "slot": "C3"},
        {"time": "11:00-11:50", "course": "CSE2048", "name": "Programming Lab", "faculty": "Dr. Smith", "venue": "SJT-Lab1", "slot": "D3"},
        {"time": "14:00-14:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": ""},
        {"time": "15:00-15:50", "course": "PHY2006", "name": "Physics", "faculty": "Dr. Taylor", "venue": "AB1-202", "slot": "G3"},
        {"time": "16:00-16:50", "course": "ENG1901", "name": "Technical English", "faculty": "Ms. Davis", "venue": "MB-205", "slot": "H3"},
        {"time": "17:00-17:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": ""}
    ],
    "Thursday": [
        {"time": "08:00-08:50", "course": "PHY2006", "name": "Physics", "faculty": "Dr. Taylor", "venue": "AB1-202", "slot": "A4"},
        {"time": "09:00-09:50", "course": "CSE2001", "name": "Computer Programming", "faculty": "Dr. Smith", "venue": "SJT101", "slot": "B4"},
        {"time": "10:00-10:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": ""},
        {"time": "11:00-11:50", "course": "MAT2001", "name": "Calculus", "faculty": "Prof. Johnson", "venue": "AB2-101", "slot": "D4"},
        {"time": "14:00-14:50", "course": "CSE2004", "name": "Data Structures", "faculty": "Dr. Wilson", "venue": "SJT102", "slot": "F4"},
        {"time": "15:00-15:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": ""},
        {"time": "16:00-16:50", "course": "ENG1901", "name": "Technical English", "faculty": "Ms. Davis", "venue": "MB-205", "slot": "H4"},
        {"time": "17:00-17:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": ""}
    ],
    "Friday": [
        {"time": "08:00-08:50", "course": "MAT2001", "name": "Calculus", "faculty": "Prof. Johnson", "venue": "AB2-101", "slot": "A5"},
        {"time": "09:00-09:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": ""},
        {"time": "10:00-10:50", "course": "CSE2001", "name": "Computer Programming", "faculty": "Dr. Smith", "venue": "SJT101", "slot": "C5"},
        {"time": "11:00-11:50", "course": "PHY2006", "name": "Physics", "faculty": "Dr. Taylor", "venue": "AB1-202", "slot": "D5"},
        {"time": "14:00-14:50", "course": "CSE2048", "name": "Programming Lab", "faculty": "Dr. Smith", "venue": "SJT-Lab1", "slot": "F5"},
        {"time": "15:00-15:50", "course": "CSE2004", "name": "Data Structures", "faculty": "Dr. Wilson", "venue": "SJT102", "slot": "G5"},
        {"time": "16:00-16:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": ""},
        {"time": "17:00-17:50", "course": "", "name": "Free Period", "faculty": "", "venue": "", "slot": ""}
    ]
}

# Course information with credits
COURSE_INFO = {
    "CSE2001": {"name": "Computer Programming", "credits": 4, "type": "Theory + Lab"},
    "CSE2004": {"name": "Data Structures", "credits": 4, "type": "Theory + Lab"},
    "CSE2048": {"name": "Programming Lab", "credits": 2, "type": "Lab"},
    "MAT2001": {"name": "Calculus", "credits": 4, "type": "Theory"},
    "PHY2006": {"name": "Physics", "credits": 3, "type": "Theory"},
    "PHY2048": {"name": "Physics Lab", "credits": 1, "type": "Lab"},
    "ENG1901": {"name": "Technical English", "credits": 3, "type": "Theory"}
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
    
    # Collect all enrolled courses from timetable
    for day_schedule in SAMPLE_TIMETABLE.values():
        for slot in day_schedule:
            if slot['course']:
                enrolled_courses.add(slot['course'])
    
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
                "venue": ""
            }
            
            # Collect slots and faculty info for this course
            for day, day_schedule in SAMPLE_TIMETABLE.items():
                for slot in day_schedule:
                    if slot['course'] == course_code:
                        course_data["slots"].append(f"{slot['slot']} ({day[:3]})")
                        if not course_data["faculty"]:
                            course_data["faculty"] = slot['faculty']
            
            course_data["slots"] = ", ".join(course_data["slots"])
            courses.append(course_data)
    
    return jsonify(courses)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)