class Teacher {
  constructor(data) {
    this.curriculum = data['Curriculum'] || data.curriculum;
    this.courseCode = data['Course Code'] || data.courseCode;
    this.courseName = data['Course Name'] || data.courseName;
    this.slot = data['Slot'] || data.slot;
    this.venue = data['Venue'] || data.venue;
    this.faculty = data['Faculty'] || data.faculty;
    this.type = data['Type'] || data.type;
  }

  // Check if this is a theory slot
  isTheory() {
    return this.type === 'TH';
  }

  // Check if this is a lab slot
  isLab() {
    return this.type === 'LAB';
  }

  // Parse slot information to get individual slots
  getSlots() {
    if (!this.slot) return [];
    
    // Handle combined slots like "C2+TC2" or "A1+L5"
    const slots = this.slot.split('+').map(s => s.trim());
    return slots;
  }

  // Get slot timing based on VIT FFCS schedule
  getSlotTimings() {
    const slotTimings = {
      // Theory slots
      'A1': { day: 'Monday', time: '08:00-08:50' },
      'A2': { day: 'Monday', time: '09:00-09:50' },
      'B1': { day: 'Tuesday', time: '08:00-08:50' },
      'B2': { day: 'Tuesday', time: '09:00-09:50' },
      'C1': { day: 'Wednesday', time: '08:00-08:50' },
      'C2': { day: 'Wednesday', time: '09:00-09:50' },
      'D1': { day: 'Thursday', time: '08:00-08:50' },
      'D2': { day: 'Thursday', time: '09:00-09:50' },
      'E1': { day: 'Friday', time: '08:00-08:50' },
      'E2': { day: 'Friday', time: '09:00-09:50' },
      'F1': { day: 'Monday', time: '10:00-10:50' },
      'F2': { day: 'Tuesday', time: '10:00-10:50' },
      'G1': { day: 'Wednesday', time: '10:00-10:50' },
      'G2': { day: 'Thursday', time: '10:00-10:50' },
      // Lab slots (typically 2-3 hours)
      'L1': { day: 'Monday', time: '08:00-10:50' },
      'L2': { day: 'Tuesday', time: '08:00-10:50' },
      'L3': { day: 'Wednesday', time: '08:00-10:50' },
      'L4': { day: 'Thursday', time: '08:00-10:50' },
      'L5': { day: 'Friday', time: '08:00-10:50' },
      'L6': { day: 'Monday', time: '11:00-13:50' },
      'L7': { day: 'Tuesday', time: '11:00-13:50' },
      'L8': { day: 'Wednesday', time: '11:00-13:50' }
    };

    const slots = this.getSlots();
    return slots.map(slot => ({
      slot: slot,
      timing: slotTimings[slot] || { day: 'Unknown', time: 'Unknown' }
    }));
  }

  // Convert to JSON for API response
  toJSON() {
    return {
      curriculum: this.curriculum,
      courseCode: this.courseCode,
      courseName: this.courseName,
      slot: this.slot,
      slots: this.getSlots(),
      venue: this.venue,
      faculty: this.faculty,
      type: this.type,
      timings: this.getSlotTimings()
    };
  }
}

module.exports = Teacher;