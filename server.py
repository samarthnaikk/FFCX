#!/usr/bin/env python3
"""
Flask server for VIT FFCS Timetable
Serves CSV data with CORS support
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Path to data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def parse_csv_file(filename):
    """Parse CSV file and return data as list of dictionaries"""
    filepath = os.path.join(DATA_DIR, filename)
    data = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Warning: {filename} not found in {DATA_DIR}")
    except Exception as e:
        print(f"Error reading {filename}: {e}")
    
    return data

def load_course_data():
    """Load and process course data from CSV files"""
    # Load courses.csv for course information
    courses_data = parse_csv_file('courses.csv')
    course_info_cache = {}
    
    for row in courses_data:
        if 'Course Code' in row:
            course_code = row.get('Course Code', '')
            course_info_cache[course_code] = {
                'courseCode': course_code,
                'courseTitle': row.get('Course Title', ''),
                'courseType': row.get('Course Type', ''),
                'L': int(row.get('L', 0)) if row.get('L', '').isdigit() else 0,
                'T': int(row.get('T', 0)) if row.get('T', '').isdigit() else 0,
                'P': int(row.get('P', 0)) if row.get('P', '').isdigit() else 0,
                'J': int(row.get('J', 0)) if row.get('J', '').isdigit() else 0,
                'credits': float(row.get('Credits', 3)) if row.get('Credits', '').replace('.', '').isdigit() else 3
            }
    
    # Load all_teachers.csv for teacher assignments
    teachers_data = parse_csv_file('all_teachers.csv')
    csv_courses = []
    
    for row in teachers_data:
        course_code = row.get('Course Code', '')
        course_info = course_info_cache.get(course_code, {})
        
        course = {
            'curriculum': row.get('Curriculum', ''),
            'courseCode': course_code,
            'courseName': row.get('Course Name', ''),
            'slot': row.get('Slot', ''),
            'venue': row.get('Venue', ''),
            'faculty': row.get('Faculty', ''),
            'type': row.get('Type', 'TH'),
            'credits': course_info.get('credits', 3)
        }
        csv_courses.append(course)
    
    return csv_courses, course_info_cache

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS)"""
    return send_from_directory('.', filename)

@app.route('/api/courses')
def get_courses():
    """API endpoint to get all courses data"""
    try:
        courses, course_info = load_course_data()
        return jsonify({
            'success': True,
            'courses': courses,
            'courseInfo': course_info,
            'total': len(courses)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'courses': [],
            'courseInfo': {}
        }), 500

@app.route('/api/search')
def search_courses():
    """API endpoint to search courses"""
    from flask import request
    query = request.args.get('q', '').lower().strip()
    
    if not query:
        return jsonify({'success': True, 'courses': []})
    
    try:
        all_courses, _ = load_course_data()
        
        # Filter courses based on query
        filtered_courses = []
        for course in all_courses:
            if (query in course.get('courseName', '').lower() or
                query in course.get('courseCode', '').lower() or
                query in course.get('faculty', '').lower()):
                filtered_courses.append(course)
        
        return jsonify({
            'success': True,
            'courses': filtered_courses[:50],  # Limit to 50 results
            'total': len(filtered_courses)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'courses': []
        }), 500

@app.route('/api/faculty')
def get_faculty():
    """API endpoint to get all faculty members"""
    try:
        courses, _ = load_course_data()
        faculty_set = set()
        
        for course in courses:
            faculty = course.get('faculty', '').strip()
            if faculty:
                faculty_set.add(faculty)
        
        faculty_list = sorted(list(faculty_set))
        
        return jsonify({
            'success': True,
            'faculty': faculty_list,
            'total': len(faculty_list)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'faculty': []
        }), 500

@app.route('/api/faculty/<faculty_name>')
def get_courses_by_faculty(faculty_name):
    """API endpoint to get courses by faculty"""
    try:
        all_courses, _ = load_course_data()
        
        # Filter courses by faculty
        faculty_courses = []
        for course in all_courses:
            if faculty_name.lower() in course.get('faculty', '').lower():
                faculty_courses.append(course)
        
        return jsonify({
            'success': True,
            'courses': faculty_courses,
            'faculty': faculty_name,
            'total': len(faculty_courses)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'courses': []
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'VIT FFCS Timetable API'
    })

if __name__ == '__main__':
    print("Starting VIT FFCS Timetable Server...")
    print(f"Data directory: {DATA_DIR}")
    print("Server will be available at: http://localhost:5000")
    print("API endpoints:")
    print("  GET /api/courses - Get all courses")
    print("  GET /api/search?q=<query> - Search courses")
    print("  GET /api/faculty - Get all faculty")
    print("  GET /api/faculty/<name> - Get courses by faculty")
    
    app.run(debug=True, host='0.0.0.0', port=5000)