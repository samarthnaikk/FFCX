# Helper functions for time parsing and slot conflict detection
from collections import defaultdict


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


def generate_slot_conflicts(timetable_template):
    """Generate comprehensive slot conflicts based on actual time overlaps.

    This function collects all time ranges where a given slot appears (a slot may appear
    in multiple day/time entries). It then marks two slots as conflicting if any of their
    time ranges overlap ON THE SAME DAY.
    """
    slot_ranges = defaultdict(list)  # slot -> list of (day, start, end)

    # Collect ranges for each slot across timetable with day information
    for day, schedule in timetable_template.items():
        for slot_info in schedule:
            available_slots = [s.strip() for s in slot_info['available_slots'].split('/')]
            theory_range = parse_time_range(slot_info.get('theory_time', ''))
            lab_range = parse_time_range(slot_info.get('lab_time', ''))

            for s in available_slots:
                if not s or s == '-':
                    continue
                if s.startswith('L'):
                    if lab_range[0] is not None:
                        slot_ranges[s].append((day, lab_range[0], lab_range[1]))
                else:
                    if theory_range[0] is not None:
                        slot_ranges[s].append((day, theory_range[0], theory_range[1]))

    # Build conflict map
    conflicts = {s: [] for s in slot_ranges}

    slots = list(slot_ranges.keys())
    for i, s1 in enumerate(slots):
        for j, s2 in enumerate(slots):
            if s1 == s2:
                continue
            # If any range of s1 overlaps any range of s2 ON THE SAME DAY, they conflict
            overlap_found = False
            for day1, start1, end1 in slot_ranges[s1]:
                for day2, start2, end2 in slot_ranges[s2]:
                    # Only check for conflicts on the same day
                    if day1 == day2 and range_overlap((start1, end1), (start2, end2)):
                        overlap_found = True
                        break
                if overlap_found:
                    break
            if overlap_found:
                conflicts[s1].append(s2)

    return conflicts


def get_conflict_details(slot1, slot2, timetable_template):
    """Get detailed information about where two slots conflict"""
    conflicts = []
    
    # Find all instances of both slots in the timetable
    slot1_instances = []
    slot2_instances = []
    
    for day, schedule in timetable_template.items():
        for time_index, slot_info in enumerate(schedule):
            available_slots = [s.strip() for s in slot_info['available_slots'].split('/')]
            
            if slot1 in available_slots:
                slot1_instances.append({
                    'day': day,
                    'time': slot_info['time'],
                    'theory_time': slot_info.get('theory_time', ''),
                    'lab_time': slot_info.get('lab_time', '')
                })
            
            if slot2 in available_slots:
                slot2_instances.append({
                    'day': day,
                    'time': slot_info['time'],
                    'theory_time': slot_info.get('theory_time', ''),
                    'lab_time': slot_info.get('lab_time', '')
                })
    
    # Check for conflicts between instances
    for s1_instance in slot1_instances:
        for s2_instance in slot2_instances:
            # Only check conflicts on the same day
            if s1_instance['day'] == s2_instance['day']:
                # Get the appropriate time ranges
                s1_time_range = parse_time_range(s1_instance['lab_time'] if slot1.startswith('L') else s1_instance['theory_time'])
                s2_time_range = parse_time_range(s2_instance['lab_time'] if slot2.startswith('L') else s2_instance['theory_time'])
                
                # Check if they overlap
                if s1_time_range[0] is not None and s2_time_range[0] is not None:
                    if range_overlap(s1_time_range, s2_time_range):
                        s1_actual_time = s1_instance['lab_time'] if slot1.startswith('L') else s1_instance['theory_time']
                        s2_actual_time = s2_instance['lab_time'] if slot2.startswith('L') else s2_instance['theory_time']
                        
                        conflicts.append({
                            'day': s1_instance['day'],
                            'slot1_time': s1_actual_time,
                            'slot2_time': s2_actual_time,
                            'slot1_type': 'Lab' if slot1.startswith('L') else 'Theory',
                            'slot2_type': 'Lab' if slot2.startswith('L') else 'Theory'
                        })
    
    return conflicts