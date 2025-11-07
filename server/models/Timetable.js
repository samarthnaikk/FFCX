class Timetable {
  constructor() {
    this.schedule = {
      Monday: {},
      Tuesday: {},
      Wednesday: {},
      Thursday: {},
      Friday: {}
    };
    this.courses = [];
    this.conflicts = [];
  }

  // Add a course to the timetable
  addCourse(course, teacher, slots) {
    const courseEntry = {
      id: Date.now() + Math.random(), // Temporary ID generation
      course: course,
      teacher: teacher,
      slots: slots,
      addedAt: new Date().toISOString()
    };

    // Check for conflicts before adding
    const conflicts = this.checkConflicts(slots);
    if (conflicts.length > 0) {
      this.conflicts.push(...conflicts);
      return { success: false, conflicts: conflicts };
    }

    // Add course to schedule
    slots.forEach(slotInfo => {
      const { slot, timing } = slotInfo;
      if (timing && timing.day !== 'Unknown') {
        if (!this.schedule[timing.day][slot]) {
          this.schedule[timing.day][slot] = [];
        }
        this.schedule[timing.day][slot].push({
          courseCode: course.courseCode,
          courseTitle: course.courseTitle,
          faculty: teacher.faculty,
          venue: teacher.venue,
          type: teacher.type,
          time: timing.time,
          credits: course.credits
        });
      }
    });

    this.courses.push(courseEntry);
    return { success: true, courseId: courseEntry.id };
  }

  // Check for slot conflicts
  checkConflicts(newSlots) {
    const conflicts = [];
    
    newSlots.forEach(slotInfo => {
      const { slot, timing } = slotInfo;
      if (timing && timing.day !== 'Unknown') {
        if (this.schedule[timing.day][slot] && this.schedule[timing.day][slot].length > 0) {
          conflicts.push({
            slot: slot,
            day: timing.day,
            time: timing.time,
            existingCourse: this.schedule[timing.day][slot][0].courseCode,
            message: `Conflict detected: Slot ${slot} on ${timing.day} is already occupied`
          });
        }
      }
    });

    return conflicts;
  }

  // Remove a course from the timetable
  removeCourse(courseId) {
    const courseIndex = this.courses.findIndex(c => c.id === courseId);
    if (courseIndex === -1) {
      return { success: false, message: 'Course not found' };
    }

    const course = this.courses[courseIndex];
    
    // Remove from schedule
    course.slots.forEach(slotInfo => {
      const { slot, timing } = slotInfo;
      if (timing && timing.day !== 'Unknown' && this.schedule[timing.day][slot]) {
        this.schedule[timing.day][slot] = this.schedule[timing.day][slot]
          .filter(entry => entry.courseCode !== course.course.courseCode);
        
        if (this.schedule[timing.day][slot].length === 0) {
          delete this.schedule[timing.day][slot];
        }
      }
    });

    // Remove from courses array
    this.courses.splice(courseIndex, 1);
    
    return { success: true };
  }

  // Get current schedule
  getSchedule() {
    return this.schedule;
  }

  // Get enrolled courses
  getCourses() {
    return this.courses;
  }

  // Get total credits
  getTotalCredits() {
    return this.courses.reduce((total, courseEntry) => {
      return total + (courseEntry.course.credits || 0);
    }, 0);
  }

  // Clear entire timetable
  clear() {
    this.schedule = {
      Monday: {},
      Tuesday: {},
      Wednesday: {},
      Thursday: {},
      Friday: {}
    };
    this.courses = [];
    this.conflicts = [];
  }

  // Generate timetable summary
  getSummary() {
    return {
      totalCourses: this.courses.length,
      totalCredits: this.getTotalCredits(),
      schedule: this.schedule,
      courses: this.courses.map(c => ({
        courseCode: c.course.courseCode,
        courseTitle: c.course.courseTitle,
        faculty: c.teacher.faculty,
        credits: c.course.credits,
        slots: c.slots.map(s => s.slot).join('+')
      })),
      conflicts: this.conflicts
    };
  }

  // Convert to JSON
  toJSON() {
    return {
      schedule: this.schedule,
      courses: this.courses,
      summary: this.getSummary(),
      lastUpdated: new Date().toISOString()
    };
  }
}

module.exports = Timetable;