// Drag and Drop functionality
const dragDropMethods = {
    // Drag state variables
    draggedCourse: null,
    draggedSlot: null,
    draggedDay: null,
    draggedIndex: -1,
    isDragging: false,

    // Drag event handlers
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

    // Drag validation methods
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

    // Course movement
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

    // Cleanup
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
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = dragDropMethods;
} else if (typeof window !== 'undefined') {
    window.dragDropMethods = dragDropMethods;
}