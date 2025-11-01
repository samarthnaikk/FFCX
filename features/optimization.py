# Timetable optimization features
from helpers.time_utils import get_conflict_details


def optimize_timetable_logic(preferences, timetable_template, slot_conflicts):
    """
    Core optimization logic for timetable generation based on preferences and priorities
    
    Args:
        preferences: Dictionary containing course preferences with priorities and teacher options
        timetable_template: The timetable template to modify
        slot_conflicts: Dictionary containing slot conflict mappings
    
    Returns:
        Dict containing optimization results
    """
    # Simple optimization algorithm
    # Clear current timetable
    for day in timetable_template:
        for slot_index in range(len(timetable_template[day])):
            timetable_template[day][slot_index].update({
                'course': '',
                'name': '',
                'faculty': '',
                'venue': '',
                'slot': '',
                'course_code': '',
                'course_type': '',
                'credits': 0
            })

    # Sort courses by priority (lower number = higher priority)
    sorted_courses = []
    for course_name, pref in preferences.items():
        sorted_courses.append({
            'name': course_name,
            'priority': pref.get('priority', 5),
            'teacher_options': pref.get('teacherOptions', [])
        })

    # Sort by priority: lower numbers first (higher priority)
    sorted_courses.sort(key=lambda x: x['priority'])

    assigned_courses = []
    failed_courses = []
    occupied_slots = set()

    print(f"Starting optimization with {len(sorted_courses)} courses:")
    for course in sorted_courses:
        print(f"  - {course['name']} (priority: {course['priority']})")

    for course in sorted_courses:
        course_name = course['name']
        teacher_options = course['teacher_options']

        print(f"\nProcessing course: {course_name} (priority: {course['priority']})")

        if not teacher_options:
            failed_courses.append(f"{course_name}: No teacher options provided")
            print(f"  FAILED: No teacher options")
            continue

        # Sort teacher options by priority (lower number = higher priority)
        teacher_options.sort(key=lambda x: x.get('priority', 5))

        print(f"  Teacher options ({len(teacher_options)}):")
        for i, option in enumerate(teacher_options):
            print(f"    {i+1}. {option.get('faculty', 'N/A')} - {option.get('slots', 'N/A')} (priority: {option.get('priority', 5)})")

        assigned = False
        for option_idx, option in enumerate(teacher_options):
            slots = option.get('slots', '').strip()
            faculty = option.get('faculty', '').strip()
            venue = option.get('venue', '').strip()

            print(f"  Trying option {option_idx+1}: {faculty} for slots {slots}")

            if not slots or not faculty:
                print(f"    SKIP: Missing slots or faculty")
                continue

            # Parse multiple slots (e.g., "A1+B1" or "A1, B1")
            slot_list = []
            if '+' in slots:
                slot_list = [s.strip().upper() for s in slots.split('+')]
            elif ',' in slots:
                slot_list = [s.strip().upper() for s in slots.split(',')]
            else:
                slot_list = [slots.upper()]

            # Check if any of the slots are already occupied or conflict
            conflict = False
            conflict_reason = ""

            for slot in slot_list:
                if slot in occupied_slots:
                    conflict = True
                    conflict_reason = f"slot {slot} already occupied"
                    break
                # Check for slot conflicts
                if slot in slot_conflicts:
                    for occupied_slot in occupied_slots:
                        if occupied_slot in slot_conflicts[slot]:
                            conflict = True
                            conflict_reason = f"slot {slot} conflicts with occupied slot {occupied_slot}"
                            break
                if conflict:
                    break

            if conflict:
                print(f"    CONFLICT: {conflict_reason}")
            else:
                print(f"    ATTEMPTING assignment to slots: {slot_list}")
                # Try to assign this course to the timetable
                success = assign_course_to_slots(course_name, slot_list, faculty, venue, timetable_template)
                if success:
                    occupied_slots.update(slot_list)
                    assigned_courses.append(f"{course_name} -> {faculty} ({', '.join(slot_list)})")
                    assigned = True
                    print(f"    SUCCESS: Assigned to {', '.join(slot_list)}")
                    break
                else:
                    print(f"    FAILED: Could not assign to timetable slots")

        if not assigned:
            failed_courses.append(f"{course_name}: No available non-conflicting slots found")
            print(f"  FINAL RESULT: FAILED - No available slots")

    message = f"Assigned {len(assigned_courses)} courses"
    if failed_courses:
        message += f", {len(failed_courses)} failed"

    # Check for clashes in the final timetable
    clashes = check_timetable_clashes(timetable_template, slot_conflicts)

    # Update message if clashes found
    if clashes:
        message += f" ⚠️ {len(clashes)} clash(es) detected!"

    return {
        'success': len(failed_courses) == 0 and len(clashes) == 0,
        'message': message,
        'assigned': assigned_courses,
        'failed': failed_courses,
        'clashes': clashes
    }


def assign_course_to_slots(course_name, slot_list, faculty, venue, timetable_template):
    """Helper function to assign a course to specific slots in the timetable"""
    try:
        # Create unique course identifier
        course_id = f"{course_name}_{'+'.join(slot_list)}"

        # Find ALL matching slots for each slot in the list
        all_slots_to_fill = []
        for slot in slot_list:
            slots_for_this_slot = []
            for day in timetable_template:
                for slot_index, time_slot in enumerate(timetable_template[day]):
                    available_options = time_slot['available_slots'].split('/')

                    if slot in available_options and not time_slot['course']:
                        slots_for_this_slot.append((day, slot_index, slot))

            if not slots_for_this_slot:
                print(f"    ERROR: Could not find any available slot {slot} in timetable")
                return False

            all_slots_to_fill.extend(slots_for_this_slot)

        # If we found all required slots, fill them ALL
        filled_count = 0
        for day, slot_index, slot in all_slots_to_fill:
            timetable_template[day][slot_index].update({
                'course': course_id,
                'name': course_name,
                'faculty': faculty,
                'venue': venue,
                'slot': slot,
                'course_code': course_name,  # Use course name as code for now
                'course_type': 'Theory' if slot.startswith(('A', 'B', 'C', 'D', 'E', 'F', 'G')) else 'Lab',
                'credits': 3  # Default credits
            })
            filled_count += 1
            print(f"    FILLED: {day} slot {slot_index} with {course_name} ({slot})")

        print(f"    TOTAL FILLED: {filled_count} slots for {course_name}")
        return filled_count > 0
    except Exception as e:
        print(f"    EXCEPTION in assign_course_to_slots: {str(e)}")
        return False


def check_timetable_clashes(timetable_template, slot_conflicts):
    """Check for clashes in the current timetable using existing validation logic"""
    enrolled_slots = set()
    conflicts = []

    # Collect all enrolled slots
    for day_schedule in timetable_template.values():
        for slot in day_schedule:
            if slot['course'] and slot['slot']:
                enrolled_slots.add(slot['slot'])

    # Check for conflicts
    for slot in enrolled_slots:
        if slot in slot_conflicts:
            conflicting_slots = slot_conflicts[slot]
            for conflict in conflicting_slots:
                if conflict in enrolled_slots:
                    # Avoid duplicate conflicts (A conflicts with B is same as B conflicts with A)
                    conflict_pair = tuple(sorted([slot, conflict]))
                    if not any(tuple(sorted([c['slot1'], c['slot2']])) == conflict_pair for c in conflicts):
                        conflicts.append({
                            "slot1": slot,
                            "slot2": conflict,
                            "message": f"Slot {slot} conflicts with {conflict}"
                        })

    return conflicts


def move_course_logic(from_day, from_index, to_day, to_index, course_data, timetable_template, slot_conflicts):
    """
    Logic for moving a course from one time slot to another
    
    Returns:
        Tuple (success: bool, message: str)
    """
    # Validate input data
    if not all([from_day, to_day, course_data]):
        return False, 'Missing required data'

    if from_day not in timetable_template or to_day not in timetable_template:
        return False, 'Invalid day specified'

    if (from_index < 0 or from_index >= len(timetable_template[from_day]) or 
        to_index < 0 or to_index >= len(timetable_template[to_day])):
        return False, 'Invalid time slot index'

    # Get source and target slots
    source_slot = timetable_template[from_day][from_index]
    target_slot = timetable_template[to_day][to_index]

    # Verify source slot has the expected course
    if not source_slot.get('course') or source_slot.get('name') != course_data.get('name'):
        return False, 'Source slot does not match expected course'

    # Check if target slot is occupied (unless moving to same slot)
    if target_slot.get('course') and not (from_day == to_day and from_index == to_index):
        return False, 'Target slot is already occupied'

    # Check if the course can fit in the target slot (slot compatibility)
    course_slot = course_data.get('slot')
    target_available_slots = target_slot.get('available_slots', '')

    if course_slot and not course_slot in target_available_slots.split('/'):
        return False, f'Course slot {course_slot} is not available in this time period'

    # Check for slot conflicts before moving
    if course_slot and course_slot in slot_conflicts:
        conflict_slots = slot_conflicts[course_slot]
        
        # Check if any conflicting slots are occupied on the same day
        for day_slot in timetable_template[to_day]:
            if day_slot.get('slot') in conflict_slots and day_slot.get('course'):
                # Allow moving to the same slot we're vacating
                if not (from_day == to_day and day_slot == source_slot):
                    return False, f'Moving would create conflict with {day_slot.get("slot")} slot on {to_day}'

    # Perform the move
    # Clear source slot
    source_slot.update({
        'course': '',
        'name': '',
        'faculty': '',
        'venue': '',
        'slot': '',
        'course_code': '',
        'course_type': '',
        'credits': 0
    })

    # Fill target slot
    target_slot.update({
        'course': course_data.get('course', ''),
        'name': course_data.get('name', ''),
        'faculty': course_data.get('faculty', ''),
        'venue': course_data.get('venue', ''),
        'slot': course_data.get('slot', ''),
        'course_code': course_data.get('course_code', ''),
        'course_type': course_data.get('course_type', ''),
        'credits': course_data.get('credits', 0)
    })

    return True, f'Successfully moved {course_data.get("name")} from {from_day} to {to_day}'