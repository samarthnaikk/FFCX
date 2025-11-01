# Data loading helper functions
import csv
import os


def load_courses_from_ref2(teachers_by_course):
    """Load courses from ref2.txt file and enrich with ALL details from all_teachers.csv"""
    courses = []
    txt_path = os.path.join(os.path.dirname(__file__), '..', 'ref2.txt')
    
    if not os.path.exists(txt_path):
        print("Warning: ref2.txt not found")
        return courses
    
    try:
        with open(txt_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                course_name = line.strip()
                # Skip empty lines
                if not course_name:
                    continue
                    
                # Default values
                course_code = ""
                course_type = "Theory Only"
                credits = 3.0
                available_slots = []
                available_venues = []
                available_faculty = []
                
                # Extract ALL details from TEACHERS_BY_COURSE
                if course_name in teachers_by_course:
                    teacher_data = teachers_by_course[course_name]
                    course_code = teacher_data.get('course_code', '')
                    teachers = teacher_data.get('teachers', [])
                    
                    # Get credits from CSV data if available
                    csv_credits = teacher_data.get('credits', None)
                    if csv_credits is not None:
                        credits = float(csv_credits)
                    
                    if teachers:
                        # Collect all unique slots, venues, and faculty
                        slots_set = set()
                        venues_set = set()
                        faculty_set = set()
                        
                        for teacher in teachers:
                            slot = teacher.get('slot', '').strip()
                            venue = teacher.get('venue', '').strip()
                            faculty = teacher.get('faculty', '').strip()
                            
                            if slot:
                                slots_set.add(slot)
                            if venue:
                                venues_set.add(venue)
                            if faculty:
                                faculty_set.add(faculty)
                        
                        available_slots = sorted(list(slots_set))
                        available_venues = sorted(list(venues_set))
                        available_faculty = sorted(list(faculty_set))
                        
                        # Determine course type based on slot analysis
                        has_lab = any('L' in slot for slot in available_slots)
                        has_theory = any('L' not in slot for slot in available_slots)
                        
                        if has_lab and has_theory:
                            course_type = "Embedded Theory and Lab"
                        elif has_lab:
                            course_type = "Lab Only"
                        else:
                            course_type = "Theory Only"
                        
                        # Only estimate credits if not loaded from CSV
                        if csv_credits is None:
                            # Estimate credits based on type (fallback)
                            if course_type == "Embedded Theory and Lab":
                                credits = 4.0
                            elif course_type == "Lab Only":
                                credits = 1.0
                            else:
                                credits = 3.0
                
                course = {
                    'course_code': course_code,
                    'title': course_name,
                    'type': course_type,
                    'credits': credits,
                    'available_slots': available_slots,
                    'available_venues': available_venues,
                    'available_faculty': available_faculty,
                    'total_options': len(teachers_by_course.get(course_name, {}).get('teachers', []))
                }
                courses.append(course)
                
        print(f"Loaded {len(courses)} courses from ref2.txt with detailed information")
        
        # Log some statistics
        courses_with_data = [c for c in courses if c['total_options'] > 0]
        print(f"Courses with teacher data: {len(courses_with_data)}/{len(courses)}")
        
    except Exception as e:
        print(f"Error loading ref2.txt: {e}")
    
    return courses


def load_teachers_from_csv():
    """Load teacher data from all_teachers.csv file and organize by course"""
    teachers_by_course = {}
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'all_teachers.csv')
    
    if not os.path.exists(csv_path):
        return teachers_by_course
    
    # Load credits from courses.csv
    credits_by_course_code = {}
    courses_csv_path = os.path.join(os.path.dirname(__file__), '..', 'courses.csv')
    if os.path.exists(courses_csv_path):
        try:
            with open(courses_csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    course_code = row.get('Course Code', '').strip()
                    credits_str = row.get('Credits', '').strip()
                    if course_code and credits_str:
                        try:
                            credits_by_course_code[course_code] = float(credits_str)
                        except (ValueError, TypeError):
                            pass
            print(f"Loaded credits for {len(credits_by_course_code)} courses from courses.csv")
        except Exception as e:
            print(f"Warning: Could not load credits from courses.csv: {e}")
    
    # Map foreign language codes to BFLE200L (Foreign Language basket course - 2.0 credits)
    foreign_language_credits = credits_by_course_code.get('BFLE200L', 2.0)
    foreign_language_codes = ['BARB101L', 'BCHI101L', 'BESP101L', 'BFRE101L', 'BGER101L', 'BJAP101L']
    for lang_code in foreign_language_codes:
        if lang_code not in credits_by_course_code:
            credits_by_course_code[lang_code] = foreign_language_credits
    
    print(f"Mapped {len(foreign_language_codes)} foreign language courses to {foreign_language_credits} credits")
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Skip empty rows
                if not row.get('Course Name', '').strip():
                    continue
                    
                course_name = row.get('Course Name', '').strip()
                course_code = row.get('Course Code', '').strip()
                faculty = row.get('Faculty', '').strip()
                slot = row.get('Slot', '').strip()
                venue = row.get('Venue', '').strip()
                course_type = row.get('Type', '').strip()
                
                # Get credits from courses.csv if available
                credits = credits_by_course_code.get(course_code, None)
                
                # Create course entry if it doesn't exist
                if course_name not in teachers_by_course:
                    teachers_by_course[course_name] = {
                        'course_code': course_code,
                        'course_name': course_name,
                        'credits': credits,  # Store credits at course level
                        'teachers': []
                    }
                
                # Check if this teacher-slot combination already exists
                existing_teacher = None
                for teacher in teachers_by_course[course_name]['teachers']:
                    if teacher['faculty'] == faculty and teacher['slot'] == slot and teacher['venue'] == venue:
                        existing_teacher = teacher
                        break
                
                # If not found, add new teacher option with sequential priority
                if not existing_teacher:
                    # Calculate priority based on current number of teachers for this course
                    priority = len(teachers_by_course[course_name]['teachers']) + 1
                    
                    teachers_by_course[course_name]['teachers'].append({
                        'faculty': faculty,
                        'slot': slot,
                        'venue': venue,
                        'type': course_type,
                        'priority': priority  # Sequential priority: 1, 2, 3, ...
                    })
                    
    except Exception as e:
        print(f"Error loading all_teachers.csv: {e}")
    
    return teachers_by_course