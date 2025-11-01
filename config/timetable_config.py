# Timetable slot and hour configuration

theory_hours = [
    "8:00 AM to 8:50 AM",
    "9:00 AM to 9:50 AM",
    "10:00 AM to 10:50 AM",
    "11:00 AM to 11:50 AM",
    "12:00 PM to 12:50 PM",
    "2:00 PM to 2:50 PM",
    "3:00 PM to 3:50 PM",
    "4:00 PM to 4:50 PM",
    "5:00 PM to 5:50 PM",
    "6:00 PM to 6:50 PM",
    "6:51 PM to 7:00 PM",
    "7:01 PM to 7:50 PM"
]

lab_hours = [
    "08:00 AM to 08:50 AM",
    "08:51 AM to 09:40 AM",
    "09:51 AM to 10:40 AM",
    "10:41 AM to 11:30 AM",
    "11:40 AM to 12:30 PM",
    "12:31 PM to 1:20 PM",
    "2:00 PM to 2:50 PM",
    "2:51 PM to 3:40 PM",
    "3:51 PM to 4:40 PM",
    "4:41 PM to 5:30 PM",
    "5:40 PM to 6:30 PM",
    "6:31 PM to 7:20 PM"
]

slots = {
    "Monday": ["A1/L1", "F1/L2", "D1/L3", "TB1/L4", "TG1/L5", "L6", "A2/L31", "F2/L32", "D2/L33", "TB2/L34", "TG2/L35", "L36", "V3"],
    "Tuesday": ["B1/L7", "G1/L8", "E1/L9", "TC1/L10", "TAA1/L11", "L12", "B2/L37", "G2/L38", "E2/L39", "TC2/L40", "TAA2/L41", "L42", "V4"],
    "Wednesday": ["C1/L13", "A1/L14", "F1/L15", "V1/L16", "V2/L17", "L18", "C2/L43", "A2/L44", "F2/L45", "TD2/L46", "TBB2/L47", "L48", "V5"],
    "Thursday": ["D1/L19", "B1/L20", "G1/L21", "TE1/L22", "TCC1/L23", "L24", "D2/L49", "B2/L50", "G2/L51", "TE2/L52", "TCC2/L53", "L54", "V6"],
    "Friday": ["E1/L25", "C1/L26", "TA1/L27", "TF1/L28", "TD1/L29", "L30", "E2/L55", "C2/L56", "TA2/L57", "TF2/L58", "TDD2/L59", "L60", "V7"]
}

def get_timetable():
    timetable = {}
    for day, slot_list in slots.items():
        timetable[day] = []
        for i, slot in enumerate(slot_list):
            timetable[day].append({
                "slot": slot,
                "hour": theory_hours[i] if i < len(theory_hours) else "",
                "type": "Theory" if "L" not in slot else "Lab"
            })
    return timetable
