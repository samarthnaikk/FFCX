// Vue.js Data and State Management
const VueAppData = {
    data() {
        return {
            timetable: {},
            courses: [],
            availableCourses: [],
            loading: true,
            loadingCourses: true,
            selectedSlot: null,
            selectedDay: '',
            selectedTimeIndex: -1,
            showAddModal: false,
            newCourse: {
                subject_name: '',
                course_code: '',
                course_type: '',
                credits: '',
                slot: '',
                faculty: '',
                venue: ''
            },
            courseSearchQuery: '',
            searchResults: [],
            showCourseDropdown: false,
            // Teacher suggestions for Add Course modal
            teacherSuggestions: [],
            showTeacherDropdown: false,
            teacherSearchQuery: '',
            totalCourses: 0,
            busyHours: 0,
            freeHours: 0,
            dayOrder: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            // Timetable code functionality
            generatedCode: '',
            importCode: '',
            // Dark mode
            isDarkMode: false,
            // Preferences modal
            showPreferences: false,
            preferences: {},
            newCoursePreference: {
                name: '',
                code: '',
                type: '',
                priority: 5
            },
            // Course search for preferences
            newCourseSearchQuery: '',
            preferenceSearchResults: [],
            showPreferenceCourseDropdown: false,
            loadingExport: false,
            loadingImport: false,
            copyStatus: 'Copy to clipboard',
            copyIcon: 'fas fa-copy',
            // Drag and Drop properties
            draggedCourse: null,
            draggedSlot: null,
            draggedDay: null,
            draggedIndex: -1,
            isDragging: false
        }
    }
};