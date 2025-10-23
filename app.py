from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Sample timetable data
SAMPLE_TIMETABLE = {
    "Monday": [
        {"time": "08:00-08:50", "course": "CSE2001", "name": "Computer Programming", "faculty": "Dr. Smith", "venue": "SJT101"},
        {"time": "09:00-09:50", "course": "MAT2001", "name": "Calculus", "faculty": "Prof. Johnson", "venue": "AB2-101"},
        {"time": "10:00-10:50", "course": "", "name": "Free Period", "faculty": "", "venue": ""},
        {"time": "11:00-11:50", "course": "PHY2048", "name": "Physics Lab", "faculty": "Dr. Brown", "venue": "AB2-301"},
        {"time": "14:00-14:50", "course": "ENG1901", "name": "Technical English", "faculty": "Ms. Davis", "venue": "MB-205"},
        {"time": "15:00-15:50", "course": "CSE2004", "name": "Data Structures", "faculty": "Dr. Wilson", "venue": "SJT102"},
        {"time": "16:00-16:50", "course": "", "name": "Free Period", "faculty": "", "venue": ""},
        {"time": "17:00-17:50", "course": "", "name": "Free Period", "faculty": "", "venue": ""}
    ],
    "Tuesday": [
        {"time": "08:00-08:50", "course": "MAT2001", "name": "Calculus", "faculty": "Prof. Johnson", "venue": "AB2-101"},
        {"time": "09:00-09:50", "course": "CSE2004", "name": "Data Structures", "faculty": "Dr. Wilson", "venue": "SJT102"},
        {"time": "10:00-10:50", "course": "PHY2006", "name": "Physics", "faculty": "Dr. Taylor", "venue": "AB1-202"},
        {"time": "11:00-11:50", "course": "", "name": "Free Period", "faculty": "", "venue": ""},
        {"time": "14:00-14:50", "course": "CSE2001", "name": "Computer Programming", "faculty": "Dr. Smith", "venue": "SJT101"},
        {"time": "15:00-15:50", "course": "ENG1901", "name": "Technical English", "faculty": "Ms. Davis", "venue": "MB-205"},
        {"time": "16:00-16:50", "course": "", "name": "Free Period", "faculty": "", "venue": ""},
        {"time": "17:00-17:50", "course": "", "name": "Free Period", "faculty": "", "venue": ""}
    ],
    "Wednesday": [
        {"time": "08:00-08:50", "course": "CSE2004", "name": "Data Structures", "faculty": "Dr. Wilson", "venue": "SJT102"},
        {"time": "09:00-09:50", "course": "PHY2006", "name": "Physics", "faculty": "Dr. Taylor", "venue": "AB1-202"},
        {"time": "10:00-10:50", "course": "MAT2001", "name": "Calculus", "faculty": "Prof. Johnson", "venue": "AB2-101"},
        {"time": "11:00-11:50", "course": "CSE2048", "name": "Programming Lab", "faculty": "Dr. Smith", "venue": "SJT-Lab1"},
        {"time": "14:00-14:50", "course": "", "name": "Free Period", "faculty": "", "venue": ""},
        {"time": "15:00-15:50", "course": "PHY2006", "name": "Physics", "faculty": "Dr. Taylor", "venue": "AB1-202"},
        {"time": "16:00-16:50", "course": "ENG1901", "name": "Technical English", "faculty": "Ms. Davis", "venue": "MB-205"},
        {"time": "17:00-17:50", "course": "", "name": "Free Period", "faculty": "", "venue": ""}
    ],
    "Thursday": [
        {"time": "08:00-08:50", "course": "PHY2006", "name": "Physics", "faculty": "Dr. Taylor", "venue": "AB1-202"},
        {"time": "09:00-09:50", "course": "CSE2001", "name": "Computer Programming", "faculty": "Dr. Smith", "venue": "SJT101"},
        {"time": "10:00-10:50", "course": "", "name": "Free Period", "faculty": "", "venue": ""},
        {"time": "11:00-11:50", "course": "MAT2001", "name": "Calculus", "faculty": "Prof. Johnson", "venue": "AB2-101"},
        {"time": "14:00-14:50", "course": "CSE2004", "name": "Data Structures", "faculty": "Dr. Wilson", "venue": "SJT102"},
        {"time": "15:00-15:50", "course": "", "name": "Free Period", "faculty": "", "venue": ""},
        {"time": "16:00-16:50", "course": "ENG1901", "name": "Technical English", "faculty": "Ms. Davis", "venue": "MB-205"},
        {"time": "17:00-17:50", "course": "", "name": "Free Period", "faculty": "", "venue": ""}
    ],
    "Friday": [
        {"time": "08:00-08:50", "course": "MAT2001", "name": "Calculus", "faculty": "Prof. Johnson", "venue": "AB2-101"},
        {"time": "09:00-09:50", "course": "", "name": "Free Period", "faculty": "", "venue": ""},
        {"time": "10:00-10:50", "course": "CSE2001", "name": "Computer Programming", "faculty": "Dr. Smith", "venue": "SJT101"},
        {"time": "11:00-11:50", "course": "PHY2006", "name": "Physics", "faculty": "Dr. Taylor", "venue": "AB1-202"},
        {"time": "14:00-14:50", "course": "CSE2048", "name": "Programming Lab", "faculty": "Dr. Smith", "venue": "SJT-Lab1"},
        {"time": "15:00-15:50", "course": "CSE2004", "name": "Data Structures", "faculty": "Dr. Wilson", "venue": "SJT102"},
        {"time": "16:00-16:50", "course": "", "name": "Free Period", "faculty": "", "venue": ""},
        {"time": "17:00-17:50", "course": "", "name": "Free Period", "faculty": "", "venue": ""}
    ]
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)