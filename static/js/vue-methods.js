// Vue.js Methods
const vueMethods = {
    // Data fetching methods
    async fetchTimetable() {
        try {
            const response = await fetch('/api/timetable');
            const data = await response.json();
            this.timetableData = data;
            this.calculateStats();
            console.log('Timetable loaded successfully');
        } catch (error) {
            console.error('Error fetching timetable:', error);
        }
    },

    async fetchCourses() {
        try {
            const response = await fetch('/api/courses');
            const data = await response.json();
            this.courses = data;
            console.log('Courses loaded successfully');
        } catch (error) {
            console.error('Error fetching courses:', error);
        }
    },

    // Course management methods
    async addCourse() {
        if (!this.selectedCourse || !this.selectedCourse.name) {
            alert('Please select a course first');
            return;
        }

        try {
            const response = await fetch('/api/add-course', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.selectedCourse)
            });

            const result = await response.json();
            if (result.success) {
                await this.fetchTimetable();
                this.calculateStats();
                this.selectedCourse = null;
                this.searchQuery = '';
                this.searchResults = [];
                this.showDropdown = false;
                console.log('Course added successfully');
            } else {
                alert('Error adding course: ' + result.message);
            }
        } catch (error) {
            console.error('Error adding course:', error);
            alert('Error adding course');
        }
    },

    async removeCourse(day, timeIndex) {
        if (confirm('Are you sure you want to remove this course?')) {
            try {
                const response = await fetch('/api/remove-course', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        day: day,
                        timeIndex: timeIndex
                    })
                });

                const result = await response.json();
                if (result.success) {
                    await this.fetchTimetable();
                    this.calculateStats();
                    console.log('Course removed successfully');
                } else {
                    alert('Error removing course: ' + result.message);
                }
            } catch (error) {
                console.error('Error removing course:', error);
                alert('Error removing course');
            }
        }
    },

    async clearTimetable() {
        if (confirm('Are you sure you want to clear the entire timetable? This cannot be undone.')) {
            try {
                const response = await fetch('/api/clear-timetable', {
                    method: 'POST'
                });

                const result = await response.json();
                if (result.success) {
                    await this.fetchTimetable();
                    this.calculateStats();
                    console.log('Timetable cleared successfully');
                } else {
                    alert('Error clearing timetable: ' + result.message);
                }
            } catch (error) {
                console.error('Error clearing timetable:', error);
                alert('Error clearing timetable');
            }
        }
    },

    // Search methods
    async searchCourses() {
        if (this.searchQuery.length < 2) {
            this.searchResults = [];
            this.showDropdown = false;
            return;
        }

        try {
            const response = await fetch(`/api/search-courses?q=${encodeURIComponent(this.searchQuery)}`);
            const results = await response.json();
            this.searchResults = results;
            this.showDropdown = results.length > 0;
        } catch (error) {
            console.error('Error searching courses:', error);
            this.searchResults = [];
            this.showDropdown = false;
        }
    },

    selectCourse(course) {
        this.selectedCourse = course;
        this.searchQuery = course.title;
        this.showDropdown = false;
        this.searchResults = [];
    },

    // Teacher suggestion methods
    async fetchTeacherSuggestions(course) {
        if (!course || !course.course_code) {
            this.teacherSuggestions = [];
            return;
        }

        try {
            const response = await fetch(`/api/teacher-suggestions?course_code=${encodeURIComponent(course.course_code)}`);
            const data = await response.json();
            this.teacherSuggestions = data.suggestions || [];
        } catch (error) {
            console.error('Error fetching teacher suggestions:', error);
            this.teacherSuggestions = [];
        }
    },

    selectTeacherSuggestion(suggestion) {
        if (this.selectedCourse) {
            this.selectedCourse.faculty = suggestion.faculty;
            this.selectedCourse.slot = suggestion.slot;
            this.selectedCourse.venue = suggestion.venue;
            this.teacherSuggestions = [];
        }
    },

    // Statistics calculation
    calculateStats() {
        let enrolledCredits = 0;
        let totalSlots = 0;
        let occupiedSlots = 0;

        // Calculate from timetable data
        if (this.timetableData && this.timetableData.timetable) {
            Object.values(this.timetableData.timetable).forEach(daySlots => {
                daySlots.forEach(slot => {
                    totalSlots++;
                    if (slot.course) {
                        occupiedSlots++;
                        // Try to get credits from the course info
                        const credits = parseFloat(slot.credits) || 0;
                        enrolledCredits += credits;
                    }
                });
            });
        }

        this.stats.enrolledCredits = enrolledCredits;
        this.stats.occupiedSlots = occupiedSlots;
        this.stats.totalSlots = totalSlots;
        this.stats.freeSlots = totalSlots - occupiedSlots;
    },

    // Export/Import methods
    async exportTimetable() {
        this.loadingExport = true;
        
        try {
            const response = await fetch('/api/export-timetable', {
                method: 'POST'
            });

            const result = await response.json();
            
            if (result.success) {
                this.generatedCode = result.code;
                this.showExportModal = true;
            } else {
                alert('Error exporting timetable: ' + result.message);
            }
        } catch (error) {
            console.error('Error exporting timetable:', error);
            alert('Error exporting timetable');
        } finally {
            this.loadingExport = false;
        }
    },

    closeExportModal() {
        this.showExportModal = false;
        this.generatedCode = '';
        this.copyStatus = 'Copy to clipboard';
        this.copyIcon = 'fas fa-copy';
    },

    showImportModal() {
        this.showImportModalFlag = true;
        this.importCode = '';
    },

    closeImportModal() {
        this.showImportModalFlag = false;
        this.importCode = '';
    },

    async importTimetable() {
        if (!this.importCode.trim()) {
            alert('Please enter a timetable code');
            return;
        }

        this.loadingImport = true;
        
        try {
            const response = await fetch('/api/import-timetable', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ code: this.importCode })
            });

            const result = await response.json();
            
            if (result.success) {
                // Refresh timetable and courses
                await this.fetchTimetable();
                await this.fetchCourses();
                this.importCode = '';
                alert(result.message);
            } else {
                alert('Error importing timetable: ' + result.message);
            }
        } catch (error) {
            console.error('Error importing timetable:', error);
            alert('Error importing timetable');
        } finally {
            this.loadingImport = false;
        }
    },

    async copyCode() {
        if (!this.generatedCode) {
            return;
        }

        try {
            await navigator.clipboard.writeText(this.generatedCode);
            this.copyStatus = 'Copied!';
            this.copyIcon = 'fas fa-check text-success';
            
            setTimeout(() => {
                this.copyStatus = 'Copy to clipboard';
                this.copyIcon = 'fas fa-copy';
            }, 2000);
        } catch (error) {
            // Fallback for browsers that don't support clipboard API
            const textArea = document.createElement('textarea');
            textArea.value = this.generatedCode;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            
            this.copyStatus = 'Copied!';
            this.copyIcon = 'fas fa-check text-success';
            
            setTimeout(() => {
                this.copyStatus = 'Copy to clipboard';
                this.copyIcon = 'fas fa-copy';
            }, 2000);
        }
    },

    // Preferences methods
    showPreferencesModal() {
        this.initializePreferences();
        this.showPreferences = true;
    },

    closePreferencesModal() {
        this.showPreferences = false;
    },

    initializePreferences() {
        // Load saved preferences from localStorage
        const saved = localStorage.getItem('ffcx_preferences');
        if (saved) {
            try {
                this.preferences = JSON.parse(saved);
            } catch (e) {
                this.preferences = {};
            }
        }

        // Initialize preferences for current courses if not already present
        this.courses.forEach(course => {
            const key = course.name || course.course_code;
            if (!this.preferences[key]) {
                this.preferences[key] = {
                    priority: 5,
                    code: course.course_code,
                    teacherOptions: [{
                        faculty: course.faculty || '',
                        slots: course.slots || '',
                        venue: course.venue || '',
                        priority: 5
                    }]
                };
            }
        });
    },

    addNewCoursePreference() {
        const courseName = this.newCourseSearchQuery.trim() || this.newCoursePreference.name.trim();
        
        if (!courseName) {
            alert('Please enter a course name');
            return;
        }
        
        if (this.preferences[courseName]) {
            alert('Course preference already exists');
            return;
        }

        // Get next available unique priority
        const uniquePriority = this.getNextAvailableCoursePriority();

        this.preferences[courseName] = {
            priority: uniquePriority,
            code: this.newCoursePreference.code.trim(),
            type: this.newCoursePreference.type.trim(),
            teacherOptions: []
        };

        // Auto-load teacher data for this course
        this.loadTeacherDataForCourse(courseName);

        // Reset form
        this.newCoursePreference = {
            name: '',
            code: '',
            type: '',
            priority: 5
        };
        this.newCourseSearchQuery = '';
        this.preferenceSearchResults = [];
        this.showPreferenceCourseDropdown = false;
    },

    async searchCoursesForPreferences() {
        if (this.newCourseSearchQuery.length < 1) {
            this.preferenceSearchResults = [];
            this.showPreferenceCourseDropdown = false;
            return;
        }

        try {
            const response = await fetch(`/api/search-courses?q=${encodeURIComponent(this.newCourseSearchQuery)}`);
            const results = await response.json();
            this.preferenceSearchResults = results;
            this.showPreferenceCourseDropdown = results.length > 0;
        } catch (error) {
            console.error('Error searching courses for preferences:', error);
            this.preferenceSearchResults = [];
            this.showPreferenceCourseDropdown = false;
        }
    },

    selectCourseForPreference(course) {
        this.newCoursePreference.name = course.title;
        this.newCoursePreference.code = course.course_code;
        this.newCoursePreference.type = course.type;
        this.newCourseSearchQuery = course.title;
        this.showPreferenceCourseDropdown = false;
        this.preferenceSearchResults = [];
        
        // Auto-load teacher data for this course
        this.loadTeacherDataForCourse(course.title);
    },

    async loadTeacherDataForCourse(courseName) {
        try {
            const response = await fetch(`/api/course-teachers?course=${encodeURIComponent(courseName)}`);
            const data = await response.json();
            
            if (data.teachers && data.teachers.length > 0) {
                // Auto-populate teacher options for this course
                const courseKey = courseName;
                
                // Create preference entry if it doesn't exist
                if (!this.preferences[courseKey]) {
                    this.preferences[courseKey] = { 
                        priority: this.newCoursePreference.priority, 
                        teacherOptions: [] 
                    };
                }
                
                // Add all available teachers as options (if not already added)
                data.teachers.forEach((teacher, index) => {
                    // Check if this teacher option already exists
                    const exists = this.preferences[courseKey].teacherOptions.some(option => 
                        option.faculty === teacher.faculty && 
                        option.slots === teacher.slot &&
                        option.venue === teacher.venue
                    );
                    
                    if (!exists) {
                        // Get next unique priority for this teacher
                        const uniquePriority = this.getNextAvailableTeacherPriority(courseKey);
                        
                        this.preferences[courseKey].teacherOptions.push({
                            faculty: teacher.faculty,
                            slots: teacher.slot,
                            venue: teacher.venue,
                            priority: uniquePriority
                        });
                    }
                });
                
                console.log(`Auto-loaded ${data.teachers.length} teacher options for ${courseName}`);
            }
        } catch (error) {
            console.error('Error loading teacher data:', error);
        }
    },

    addEnrolledCourseToPreferences(courseName) {
        // Create preference entry if it doesn't exist
        if (!this.preferences[courseName]) {
            this.preferences[courseName] = { 
                priority: this.getNextAvailableCoursePriority(), 
                teacherOptions: [] 
            };
            
            // Auto-load teacher data for this course
            this.loadTeacherDataForCourse(courseName);
        }
    },

    removeCoursePreference(courseName) {
        if (confirm(`Remove all preferences for "${courseName}"?`)) {
            delete this.preferences[courseName];
        }
    },

    addTeacherOption(courseKey) {
        if (!this.preferences[courseKey]) {
            this.preferences[courseKey] = { priority: this.getNextAvailableCoursePriority(), teacherOptions: [] };
        }
        
        // Get next available unique priority for this course's teachers
        const nextPriority = this.getNextAvailableTeacherPriority(courseKey);
        
        this.preferences[courseKey].teacherOptions.push({
            faculty: '',
            slots: '',
            venue: '',
            priority: nextPriority
        });
    },

    removeTeacherOption(courseKey, index) {
        if (this.preferences[courseKey] && this.preferences[courseKey].teacherOptions) {
            this.preferences[courseKey].teacherOptions.splice(index, 1);
        }
    },

    // Priority validation functions
    validateCoursePriority(courseName, priority) {
        if (this.hasCoursePriorityConflict(courseName, priority)) {
            alert(`Priority ${priority} is already used by another course. Please choose a different priority.`);
            // Reset to next available priority
            this.preferences[courseName].priority = this.getNextAvailableCoursePriority();
            return false;
        }
        return true;
    },

    validateTeacherPriority(courseName, teacherIndex, priority) {
        if (this.hasTeacherPriorityConflict(courseName, teacherIndex, priority)) {
            alert(`Priority ${priority} is already used by another teacher in this course. Please choose a different priority.`);
            // Reset to next available priority
            this.preferences[courseName].teacherOptions[teacherIndex].priority = this.getNextAvailableTeacherPriority(courseName);
            return false;
        }
        return true;
    },

    hasCoursePriorityConflict(currentCourseName, priority) {
        return Object.entries(this.preferences).some(([courseName, pref]) => 
            courseName !== currentCourseName && pref.priority === priority
        );
    },

    hasTeacherPriorityConflict(courseName, currentIndex, priority) {
        if (!this.preferences[courseName] || !this.preferences[courseName].teacherOptions) {
            return false;
        }
        
        return this.preferences[courseName].teacherOptions.some((option, index) => 
            index !== currentIndex && option.priority === priority
        );
    },

    getNextAvailableCoursePriority() {
        const usedPriorities = Object.values(this.preferences).map(pref => pref.priority);
        for (let i = 1; i <= 10; i++) {
            if (!usedPriorities.includes(i)) {
                return i;
            }
        }
        return 1; // Fallback
    },

    getNextAvailableTeacherPriority(courseName) {
        if (!this.preferences[courseName] || !this.preferences[courseName].teacherOptions) {
            return 1;
        }
        
        const usedPriorities = this.preferences[courseName].teacherOptions.map(option => option.priority);
        for (let i = 1; i <= 10; i++) {
            if (!usedPriorities.includes(i)) {
                return i;
            }
        }
        return 1; // Fallback
    },

    validateAllPriorities() {
        const errors = [];
        
        // Check for duplicate course priorities
        const coursePriorities = {};
        Object.entries(this.preferences).forEach(([courseName, pref]) => {
            const priority = pref.priority;
            if (coursePriorities[priority]) {
                errors.push(`• Courses "${coursePriorities[priority]}" and "${courseName}" both have priority ${priority}`);
            } else {
                coursePriorities[priority] = courseName;
            }
        });
        
        // Check for duplicate teacher priorities within each course
        Object.entries(this.preferences).forEach(([courseName, pref]) => {
            if (pref.teacherOptions && pref.teacherOptions.length > 1) {
                const teacherPriorities = {};
                pref.teacherOptions.forEach((option, index) => {
                    const priority = option.priority;
                    if (teacherPriorities[priority]) {
                        errors.push(`• Course "${courseName}": Teachers "${teacherPriorities[priority]}" and "${option.faculty}" both have priority ${priority}`);
                    } else {
                        teacherPriorities[priority] = option.faculty || `Teacher ${index + 1}`;
                    }
                });
            }
        });
        
        return errors;
    },

    canOptimize() {
        return this.validateAllPriorities().length === 0;
    },

    savePreferences() {
        localStorage.setItem('ffcx_preferences', JSON.stringify(this.preferences));
        alert('Preferences saved!');
    },

    async optimizeTimetable() {
        // Validate priorities before optimization
        const validationErrors = this.validateAllPriorities();
        if (validationErrors.length > 0) {
            alert(`❌ Cannot generate optimized timetable due to priority conflicts:\n\n${validationErrors.join('\n')}\n\nPlease fix these issues before optimizing.`);
            return;
        }

        try {
            const response = await fetch('/api/optimize-timetable', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ preferences: this.preferences })
            });

            const result = await response.json();
            
            // Always refresh the timetable and courses to show changes
            await this.fetchTimetable();
            await this.fetchCourses();
            
            if (result.success) {
                this.closePreferencesModal();
                alert(`✅ Optimization completed successfully!\n\n${result.message}\n\nAssigned:\n${result.assigned.join('\n')}`);
            } else {
                let message = `⚠️ Optimization completed with issues:\n\n${result.message}`;
                
                if (result.assigned && result.assigned.length > 0) {
                    message += `\n\n✅ Successfully assigned:\n${result.assigned.join('\n')}`;
                }
                
                if (result.failed && result.failed.length > 0) {
                    message += `\n\n❌ Failed to assign:\n${result.failed.join('\n')}`;
                }
                
                if (result.clashes && result.clashes.length > 0) {
                    message += `\n\n⚠️ Clashes detected:\n${result.clashes.map(c => c.message).join('\n')}`;
                }
                
                alert(message);
            }
        } catch (error) {
            console.error('Error optimizing timetable:', error);
            alert('Error optimizing timetable');
        }
    },

    // Drag and Drop methods
    startDrag(event, day, slot, index) {
        if (!slot.course) return; // Can't drag empty slots
        
        this.draggedCourse = slot;
        this.draggedSlot = slot;
        this.draggedDay = day;
        this.draggedIndex = index;
        this.isDragging = true;
        
        // Set drag data
        event.dataTransfer.setData('text/plain', JSON.stringify({
            day,
            index,
            course: slot
        }));
        event.dataTransfer.effectAllowed = 'move';
        
        // Add dragging class after a brief delay to avoid flickering
        setTimeout(() => {
            event.target.classList.add('dragging');
        }, 1);
    },

    onDragOver(event) {
        event.preventDefault();
        event.dataTransfer.dropEffect = 'move';
    },

    onDragEnter(event, day, slot, index) {
        if (!this.isDragging) return;
        
        event.preventDefault();
        const targetElement = event.currentTarget;
        
        // Check if this is a valid drop target
        if (this.canDropCourse(day, slot, index)) {
            targetElement.classList.add('drop-zone');
            targetElement.classList.remove('drop-invalid');
            targetElement.title = `Drop ${this.draggedCourse.name} here`;
        } else {
            targetElement.classList.add('drop-invalid');
            targetElement.classList.remove('drop-zone');
            const errorMessage = this.getDropErrorMessage(day, slot, index);
            targetElement.title = `Cannot drop: ${errorMessage}`;
        }
    },

    onDragLeave(event) {
        const targetElement = event.currentTarget;
        targetElement.classList.remove('drop-zone', 'drop-invalid');
        targetElement.title = targetElement.getAttribute('data-original-title') || '';
    },

    onDrop(event, targetDay, targetSlot, targetIndex) {
        event.preventDefault();
        
        if (!this.isDragging || !this.draggedCourse) return;
        
        const targetElement = event.currentTarget;
        targetElement.classList.remove('drop-zone', 'drop-invalid');
        
        // Check if this is a valid drop
        if (!this.canDropCourse(targetDay, targetSlot, targetIndex)) {
            const errorMessage = this.getDropErrorMessage(targetDay, targetSlot, targetIndex);
            alert(`Cannot move course here: ${errorMessage}`);
            this.endDrag();
            return;
        }
        
        // Don't drop on the same slot
        if (this.draggedDay === targetDay && this.draggedIndex === targetIndex) {
            this.endDrag();
            return;
        }
        
        this.moveCourse(targetDay, targetIndex);
    },

    onDragEnd(event) {
        this.endDrag();
        event.target.classList.remove('dragging');
    },

    endDrag() {
        this.isDragging = false;
        this.draggedCourse = null;
        this.draggedSlot = null;
        this.draggedDay = null;
        this.draggedIndex = -1;
        
        // Clean up all drag classes
        document.querySelectorAll('.drop-zone, .drop-invalid, .dragging').forEach(el => {
            el.classList.remove('drop-zone', 'drop-invalid', 'dragging');
        });
    },

    canDropCourse(targetDay, targetSlot, targetIndex) {
        if (!this.draggedCourse) return false;
        
        // Can't drop on occupied slots (unless moving to same slot)
        if (targetSlot.course && !(this.draggedDay === targetDay && this.draggedIndex === targetIndex)) {
            return false;
        }
        
        // Check if the course can fit in this time slot
        const draggedCourse = this.draggedCourse;
        const targetAvailableSlots = targetSlot.available_slots || '';
        
        // Check if the course's slot is available in this time period
        if (draggedCourse.slot && !targetAvailableSlots.includes(draggedCourse.slot)) {
            return false;
        }
        
        return true;
    },

    getDropErrorMessage(targetDay, targetSlot, targetIndex) {
        if (!this.draggedCourse) return "No course selected";
        
        // Check if dropping on occupied slot
        if (targetSlot.course && !(this.draggedDay === targetDay && this.draggedIndex === targetIndex)) {
            return `Cannot drop here: ${targetSlot.name} is already scheduled at this time`;
        }
        
        // Check slot compatibility
        const draggedCourse = this.draggedCourse;
        const targetAvailableSlots = targetSlot.available_slots || '';
        
        if (draggedCourse.slot && !targetAvailableSlots.includes(draggedCourse.slot)) {
            return `Cannot drop here: Slot ${draggedCourse.slot} is not available at this time. Available slots: ${targetAvailableSlots}`;
        }
        
        return "Drop is allowed";
    },

    async moveCourse(targetDay, targetIndex) {
        if (!this.draggedCourse) return;
        
        try {
            const response = await fetch('/api/move-course', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    from_day: this.draggedDay,
                    from_index: this.draggedIndex,
                    to_day: targetDay,
                    to_index: targetIndex,
                    course: this.draggedCourse
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Update the local timetable
                await this.fetchTimetable();
                this.calculateStats();
            } else {
                alert('Error moving course: ' + result.message);
            }
        } catch (error) {
            console.error('Error moving course:', error);
            alert('Error moving course');
        } finally {
            this.endDrag();
        }
    },

    // Dark mode toggle
    toggleDarkMode() {
        this.isDarkMode = !this.isDarkMode;
        document.documentElement.setAttribute('data-theme', this.isDarkMode ? 'dark' : 'light');
        localStorage.setItem('darkMode', this.isDarkMode);
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = vueMethods;
} else if (typeof window !== 'undefined') {
    window.vueMethods = vueMethods;
}