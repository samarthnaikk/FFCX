# Priority validation features for timetable optimization


def validate_priority_conflicts(preferences):
    """Validate that there are no duplicate priorities in courses or teachers within same course"""
    errors = []
    
    # Check for duplicate course priorities
    course_priorities = {}
    for course_name, pref in preferences.items():
        priority = pref.get('priority', 5)
        if priority in course_priorities:
            errors.append(f'Courses "{course_priorities[priority]}" and "{course_name}" both have priority {priority}')
        else:
            course_priorities[priority] = course_name
    
    # Check for duplicate teacher priorities within each course
    for course_name, pref in preferences.items():
        teacher_options = pref.get('teacherOptions', [])
        if len(teacher_options) > 1:
            teacher_priorities = {}
            for i, option in enumerate(teacher_options):
                priority = option.get('priority', 5)
                faculty = option.get('faculty', f'Teacher {i+1}')
                if priority in teacher_priorities:
                    errors.append(f'Course "{course_name}": Teachers "{teacher_priorities[priority]}" and "{faculty}" both have priority {priority}')
                else:
                    teacher_priorities[priority] = faculty
    
    return errors