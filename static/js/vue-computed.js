// Vue.js Computed Properties
const VueComputedProperties = {
    computed: {
        orderedTimetable() {
            const ordered = {};
            this.dayOrder.forEach(day => {
                if (this.timetable[day]) {
                    ordered[day] = this.timetable[day];
                }
            });
            return ordered;
        },
        totalCourseCredits() {
            // Calculate total credits from unique courses in the timetable
            const uniqueCourses = new Map(); // course name -> credits
            
            Object.values(this.timetable).forEach(day => {
                day.forEach(slot => {
                    if (slot.course && slot.name) {
                        // Store credits for each unique course name
                        if (!uniqueCourses.has(slot.name)) {
                            uniqueCourses.set(slot.name, parseFloat(slot.credits) || 0);
                        }
                    }
                });
            });
            
            // Sum up all unique course credits
            let total = 0;
            uniqueCourses.forEach(credits => {
                total += credits;
            });
            
            return total;
        },
        theoryCourses() {
            return this.courses.filter(course => course.type === 'Theory').length;
        },
        labCourses() {
            return this.courses.filter(course => course.type.includes('Lab')).length;
        },
        availableSlots() {
            if (!this.selectedSlot) return [];
            return this.selectedSlot.available_slots.split('/');
        },
        isFormValid() {
            // More flexible validation - check for content rather than exact matching
            return this.newCourse.subject_name.trim() && 
                   this.newCourse.faculty.trim() &&
                   this.newCourse.slot.trim() &&
                   this.newCourse.venue.trim();
        }
    }
};