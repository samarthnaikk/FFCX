# Course-related routes
from flask import jsonify, request
import json
import csv
import os


def register_course_routes(app, available_courses, teachers_by_course):
    """Register course-related routes"""
    
    @app.route('/api/courses')
    def get_courses():
        """Get all available courses with their details"""
        try:
            # Create a copy of the available courses list to avoid modifying the original
            courses_list = []
            
            for course in available_courses:
                # Create a copy of each course dict
                course_copy = course.copy()
                courses_list.append(course_copy)
            
            print(f"Returning {len(courses_list)} courses")
            
            # Log a few sample courses for debugging
            if courses_list:
                print(f"Sample courses:")
                for i, course in enumerate(courses_list[:3]):  # Show first 3
                    print(f"  {i+1}. {course.get('title', 'Unknown')}: {course.get('type', 'Unknown')} - {course.get('credits', 0)} credits")
                
                # Quick stats
                total_credits = sum(course.get('credits', 0) for course in courses_list)
                courses_with_teachers = len([c for c in courses_list if c.get('total_options', 0) > 0])
                print(f"Total credits available: {total_credits}")
                print(f"Courses with teacher options: {courses_with_teachers}/{len(courses_list)}")
            
            return jsonify(courses_list)
            
        except Exception as e:
            print(f"Error in get_courses: {e}")
            return jsonify([]), 500

    @app.route('/api/course-details')
    def get_course_details():
        """Get detailed information about a course"""
        course_name = request.args.get('name')
        # Implementation here - return course details from database
        return jsonify({})

    @app.route('/api/course-options/<course_name>')
    def get_course_options(course_name):
        """Get all available options (faculty, slots, venues) for a specific course"""
        if course_name in teachers_by_course:
            course_data = teachers_by_course[course_name]
            
            # Extract unique values
            options = {
                'faculty': [],
                'slots': [],
                'venues': [],
                'teachers': course_data.get('teachers', [])
            }
            
            for teacher in course_data.get('teachers', []):
                faculty = teacher.get('faculty', '').strip()
                slot = teacher.get('slot', '').strip()
                venue = teacher.get('venue', '').strip()
                
                if faculty and faculty not in options['faculty']:
                    options['faculty'].append(faculty)
                if slot and slot not in options['slots']:
                    options['slots'].append(slot)
                if venue and venue not in options['venues']:
                    options['venues'].append(venue)
            
            # Sort for consistency
            options['faculty'].sort()
            options['slots'].sort()
            options['venues'].sort()
            
            return jsonify(options)
        
        return jsonify({
            'faculty': [],
            'slots': [],
            'venues': [],
            'teachers': []
        })

    @app.route('/api/available-courses')
    def get_available_courses():
        """Get list of all available course names for search/autocomplete"""
        course_names = [course['title'] for course in available_courses if course.get('title')]
        return jsonify({'courses': sorted(course_names)})

    @app.route('/api/search-courses')
    def search_courses():
        """Search for courses by name"""
        query = request.args.get('query', '').lower()
        if not query:
            return jsonify([])
        
        matching_courses = []
        for course in available_courses:
            course_title = course.get('title', '').lower()
            course_code = course.get('course_code', '').lower()
            if query in course_title or query in course_code:
                matching_courses.append(course)
        
        return jsonify(matching_courses[:20])  # Limit to 20 results

    @app.route('/api/course-teachers')
    def get_course_teachers():
        """Get all teachers for a specific course"""
        course_name = request.args.get('course')
        
        if not course_name:
            return jsonify({'error': 'Course name is required'}), 400
        
        # Search in teachers data
        if course_name in teachers_by_course:
            course_data = teachers_by_course[course_name]
            return jsonify({
                'course_name': course_name,
                'course_code': course_data.get('course_code', ''),
                'teachers': course_data.get('teachers', [])
            })
        
        # If exact match not found, try partial matching
        partial_matches = []
        for name, data in teachers_by_course.items():
            if course_name.lower() in name.lower():
                partial_matches.append({
                    'course_name': name,
                    'course_code': data.get('course_code', ''),
                    'teachers': data.get('teachers', [])
                })
        
        if partial_matches:
            return jsonify(partial_matches[0])  # Return first match
        
        return jsonify({'teachers': []})