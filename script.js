// VIT FFCS Timetable JavaScript

// Theory and Lab hour timings from referencetext.txt
const THEORY_HOURS = [
    '8:00 AM to 8:50 AM', '9:00 AM to 9:50 AM', '10:00 AM to 10:50 AM',
    '11:00 AM to 11:50 AM', '12:00 PM to 12:50 PM', '', '',
    '2:00 PM to 2:50 PM', '3:00 PM to 3:50 PM', '4:00 PM to 4:50 PM',
    '5:00 PM to 5:50 PM', '6:00 PM to 6:50 PM', '6:51 PM to 7:00 PM', '7:01 PM to 7:50 PM'
];

const LAB_HOURS = [
    '08:00 AM to 08:50 AM', '08:51 AM to 09:40 AM', '09:51 AM to 10:40 AM',
    '10:41 AM to 11:30 AM', '11:40 AM to 12:30 PM', '12:31 PM to 1:20 PM', 'LUNCH',
    '2:00 PM to 2:50 PM', '2:51 PM to 3:40 PM', '3:51 PM to 4:40 PM',
    '4:41 PM to 5:30 PM', '5:40 PM to 6:30 PM', '6:31 PM to 7:20 PM', ''
];

const DAYS = ['MON', 'TUE', 'WED', 'THU', 'FRI'];

// VIT FFCS day-wise slot mapping from referencetext.txt
const DAY_SLOT_MAPPING = {
    MON: ['A1 / L1', 'F1 / L2', 'D1 / L3', 'TB1 / L4', 'TG1 / L5', 'L6', '', 'A2 / L31', 'F2 / L32', 'D2 / L33', 'TB2 / L34', 'TG2 / L35', 'L36', 'V3'],
    TUE: ['B1 / L7', 'G1 / L8', 'E1 / L9', 'TC1 / L10', 'TAA1 / L11', 'L12', '', 'B2 / L37', 'G2 / L38', 'E2 / L39', 'TC2 / L40', 'TAA2 / L41', 'L42', 'V4'],
    WED: ['C1 / L13', 'A1 / L14', 'F1 / L15', 'V1 / L16', 'V2 / L17', 'L18', '', 'C2 / L43', 'A2 / L44', 'F2 / L45', 'TD2 / L46', 'TBB2 / L47', 'L48', 'V5'],
    THU: ['D1 / L19', 'B1 / L20', 'G1 / L21', 'TE1 / L22', 'TCC1 / L23', 'L24', '', 'D2 / L49', 'B2 / L50', 'G2 / L51', 'TE2 / L52', 'TCC2 / L53', 'L54', 'V6'],
    FRI: ['E1 / L25', 'C1 / L26', 'TA1 / L27', 'TF1 / L28', 'TD1 / L29', 'L30', '', 'E2 / L55', 'C2 / L56', 'TA2 / L57', 'TF2 / L58', 'TDD2 / L59', 'L60', 'V7']
};

// Global variables
let csvCourses = [];
let courseInfoCache = {};
let facultyList = [];
let addedCourses = {};

// Course data structure
class Course {
    constructor(data) {
        this.courseCode = data.courseCode || '';
        this.courseName = data.courseName || '';
        this.slot = data.slot || '';
        this.venue = data.venue || '';
        this.faculty = data.faculty || '';
        this.type = data.type || 'TH';
        this.curriculum = data.curriculum || '';
        this.credits = data.credits || 3;
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeTimetable();
    initializeEventListeners();
    loadCSVData();
});

// Generate timetable grid
function initializeTimetable() {
    const tbody = document.getElementById('timetable-body');
    tbody.innerHTML = '';

    for (let i = 0; i < THEORY_HOURS.length; i++) {
        const row = document.createElement('tr');
        
        // Time cell
        const timeCell = document.createElement('td');
        timeCell.className = 'time-cell';
        timeCell.innerHTML = formatTimeCell(THEORY_HOURS[i]);
        row.appendChild(timeCell);

        // Day cells
        DAYS.forEach(day => {
            const dayCell = document.createElement('td');
            dayCell.innerHTML = renderSlotContent(DAY_SLOT_MAPPING[day][i], day, i);
            row.appendChild(dayCell);
        });

        tbody.appendChild(row);
    }
}

// Format time cell content
function formatTimeCell(timeRange) {
    if (timeRange === 'LUNCH') {
        return `<div class="lunch-badge">LUNCH</div>`;
    }
    
    if (!timeRange || timeRange === '') {
        return '';
    }

    const parts = timeRange.split(' to ');
    if (parts.length === 2) {
        return `
            <div class="time-range">
                <div class="time-start">${parts[0]}</div>
                <div class="time-separator">to</div>
                <div class="time-end">${parts[1]}</div>
            </div>
        `;
    }

    return `<div class="time-range">${timeRange}</div>`;
}

// Render slot content
function renderSlotContent(slotContent, day, timeIndex) {
    // Check for added courses first
    const daySlots = DAY_SLOT_MAPPING[day][timeIndex];
    if (daySlots) {
        const slots = daySlots.split(' / ');
        for (const slot of slots) {
            if (addedCourses[slot]) {
                const course = addedCourses[slot];
                return `
                    <div class="course-display">
                        <div class="course-code">${course.courseCode}</div>
                        <div class="course-name">${course.courseName}</div>
                        <div class="course-faculty">${course.faculty}</div>
                    </div>
                `;
            }
        }
    }

    if (!slotContent || slotContent === '') {
        return '<div style="color: rgba(255, 255, 255, 0.5);">-</div>';
    }

    return `
        <div class="slot-content">
            <div class="slot-main">${slotContent}</div>
        </div>
    `;
}

// Initialize event listeners
function initializeEventListeners() {
    const addCourseBtn = document.getElementById('addCourseBtn');
    const courseForm = document.getElementById('courseForm');
    const closeFormBtn = document.getElementById('closeFormBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const courseFormElement = document.getElementById('addCourseFormElement');
    const courseSearch = document.getElementById('courseSearch');
    const facultyInput = document.getElementById('faculty');

    addCourseBtn.addEventListener('click', () => {
        courseForm.style.display = 'block';
    });

    closeFormBtn.addEventListener('click', () => {
        courseForm.style.display = 'none';
        resetForm();
    });

    cancelBtn.addEventListener('click', () => {
        courseForm.style.display = 'none';
        resetForm();
    });

    courseFormElement.addEventListener('submit', handleFormSubmit);
    courseSearch.addEventListener('input', handleCourseSearch);
    facultyInput.addEventListener('input', handleFacultySearch);

    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.form-group')) {
            hideAllDropdowns();
        }
    });
}

// Load CSV data from Python backend
async function loadCSVData() {
    try {
        const response = await fetch('http://localhost:5000/api/courses');
        const data = await response.json();
        
        csvCourses = data.courses || [];
        courseInfoCache = data.courseInfo || {};
        facultyList = [...new Set(csvCourses.map(course => course.faculty))].sort();
        
        console.log('CSV data loaded successfully');
    } catch (error) {
        console.warn('Could not load CSV data from server, using fallback data:', error);
        
        // Fallback data
        csvCourses = [
            new Course({
                courseCode: "BCHY101L",
                courseName: "Engineering Chemistry",
                slot: "C2",
                venue: "PRP735",
                faculty: "SATHISH KUMAR P",
                type: "TH",
                curriculum: "FC - Foundation Core",
                credits: 3
            }),
            new Course({
                courseCode: "BCSE101E",
                courseName: "Computer Programming: Python",
                slot: "A1",
                venue: "SCOPE Lab1",
                faculty: "Dr. RAJESH KUMAR",
                type: "LAB",
                curriculum: "PC - Program Core",
                credits: 3
            })
        ];
        
        facultyList = [...new Set(csvCourses.map(course => course.faculty))].sort();
    }
}

// Search courses
function searchCourses(query) {
    if (!query.trim()) return [];
    
    const lowercaseQuery = query.toLowerCase().trim();
    return csvCourses.filter(course =>
        course.courseName.toLowerCase().includes(lowercaseQuery) ||
        course.courseCode.toLowerCase().includes(lowercaseQuery) ||
        course.faculty.toLowerCase().includes(lowercaseQuery)
    );
}

// Handle course search input
function handleCourseSearch(event) {
    const query = event.target.value;
    const dropdown = document.getElementById('courseDropdown');
    
    if (!query.trim()) {
        dropdown.style.display = 'none';
        return;
    }

    const results = searchCourses(query);
    displayCourseDropdown(results, dropdown);
}

// Display course search results
function displayCourseDropdown(courses, dropdown) {
    dropdown.innerHTML = '';
    
    if (courses.length === 0) {
        dropdown.style.display = 'none';
        return;
    }

    courses.slice(0, 10).forEach(course => {
        const item = document.createElement('div');
        item.className = 'dropdown-item';
        item.innerHTML = `
            <strong>${course.courseCode}</strong><br>
            <small>${course.courseName}</small><br>
            <small style="color: rgba(255, 255, 255, 0.7);">${course.faculty}</small>
        `;
        item.addEventListener('click', () => selectCourse(course));
        dropdown.appendChild(item);
    });

    dropdown.style.display = 'block';
}

// Select course from dropdown
function selectCourse(course) {
    document.getElementById('courseCode').value = course.courseCode;
    document.getElementById('courseName').value = course.courseName;
    document.getElementById('faculty').value = course.faculty;
    document.getElementById('venue').value = course.venue;
    document.getElementById('courseType').value = course.type;
    
    hideAllDropdowns();
}

// Handle faculty search
function handleFacultySearch(event) {
    const query = event.target.value;
    const dropdown = document.getElementById('facultyDropdown');
    
    if (!query.trim()) {
        dropdown.style.display = 'none';
        return;
    }

    const results = facultyList.filter(faculty =>
        faculty.toLowerCase().includes(query.toLowerCase())
    );
    
    displayFacultyDropdown(results, dropdown);
}

// Display faculty dropdown
function displayFacultyDropdown(faculties, dropdown) {
    dropdown.innerHTML = '';
    
    if (faculties.length === 0) {
        dropdown.style.display = 'none';
        return;
    }

    faculties.slice(0, 10).forEach(faculty => {
        const item = document.createElement('div');
        item.className = 'dropdown-item';
        item.textContent = faculty;
        item.addEventListener('click', () => selectFaculty(faculty));
        dropdown.appendChild(item);
    });

    dropdown.style.display = 'block';
}

// Select faculty from dropdown
function selectFaculty(faculty) {
    document.getElementById('faculty').value = faculty;
    
    // Auto-fill with first course by this faculty
    const courses = csvCourses.filter(course =>
        course.faculty.toLowerCase().includes(faculty.toLowerCase())
    );
    
    if (courses.length > 0) {
        const course = courses[0];
        document.getElementById('venue').value = course.venue;
        document.getElementById('courseType').value = course.type;
    }
    
    hideAllDropdowns();
}

// Hide all dropdowns
function hideAllDropdowns() {
    document.getElementById('courseDropdown').style.display = 'none';
    document.getElementById('facultyDropdown').style.display = 'none';
}

// Handle form submission
function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = {
        courseCode: document.getElementById('courseCode').value,
        courseName: document.getElementById('courseName').value,
        slot: document.getElementById('slot').value,
        faculty: document.getElementById('faculty').value,
        venue: document.getElementById('venue').value,
        type: document.getElementById('courseType').value
    };

    if (formData.courseCode && formData.courseName && formData.slot && formData.faculty) {
        const course = new Course(formData);
        addedCourses[course.slot] = course;
        
        // Refresh the timetable
        initializeTimetable();
        
        // Close the form
        document.getElementById('courseForm').style.display = 'none';
        resetForm();
        
        console.log('Course added:', course);
    }
}

// Reset form
function resetForm() {
    document.getElementById('addCourseFormElement').reset();
    hideAllDropdowns();
}