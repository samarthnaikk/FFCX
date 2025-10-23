# FFCX - Interactive FFCS Timetable Planner for VIT Students

## Overview

FFCX is an interactive web application designed to help VIT (Vellore Institute of Technology) students create and manage their FFCS (Fully Flexible Credit System) timetables. This platform provides an intuitive interface for course selection, conflict detection, and timetable visualization based on actual VIT FFCS slot timings.

## What is FFCS?

The Fully Flexible Credit System (FFCS) is VIT's unique academic structure that allows students to:
- Choose their own courses based on interest and career goals
- Select preferred faculty members and class timings
- Create flexible timetables with theory and lab components
- Progress at their own pace across different semesters

## Key Features

### 📅 Interactive Timetable
- **Visual Timetable Display**: Clean, responsive grid showing Monday-Friday schedule
- **Theory vs Lab Distinction**: Different color coding for theory (blue) and lab (green) sessions
- **Accurate Timing**: Based on actual VIT FFCS slot timings with proper lab hour calculations
- **Click-to-View Details**: Click any occupied slot to see course details

### 🔍 Smart Course Search
- **Autocomplete Search**: Type to search from 160+ VIT courses loaded from CSV database
- **Auto-fill Information**: Selecting a course automatically fills course code, type, and credits
- **Editable Fields**: All auto-filled fields remain editable for customization

### 🎯 Advanced Slot Management
- **Multi-Slot Support**: Add courses with multiple slots (e.g., A1+L5 for theory+lab combinations)
- **Conflict Detection**: Intelligent conflict detection between overlapping time slots
- **Lab-Theory Overlap Detection**: Prevents conflicts between lab sessions and overlapping theory classes

### 📊 Course Management
- **Add/Remove Courses**: Easy course addition with comprehensive form validation
- **Course List Display**: View all enrolled courses with credits, faculty, and venue information
- **Dynamic Statistics**: Real-time calculation of total credits from enrolled courses

### 🛡️ Smart Validation
- **Slot Conflict Prevention**: Prevents adding courses that conflict with existing schedule
- **Occupancy Checking**: Ensures slots aren't double-booked
- **Multi-slot Validation**: Validates entire slot combinations before adding

### 🎨 User Experience
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Bootstrap 5 Styling**: Modern, professional interface
- **Vue.js Interactivity**: Real-time updates without page refreshes
- **Intuitive Icons**: Clear visual indicators for different course types

## Getting Started

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/samarthnaikk/FFCX.git
   cd FFCX
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Activate your virtual environment:**
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Start the Flask server:**
   ```bash
   python app.py
   ```

3. **Open your browser and navigate to:**
   ```
   http://localhost:5001
   ```

## How to Use

### Adding Courses

1. **Click the "+" button** next to "Enrolled Courses"
2. **Search for courses** by typing in the course name field (e.g., type "data" to see Data Structures, Data Mining, etc.)
3. **Select from dropdown** to auto-fill course code, type, and credits
4. **Enter slot information**:
   - Single slot: `A1`, `B2`, `L31`
   - Multiple slots: `A1+L5`, `B1+B2`, `C1+L15+L16`
5. **Add faculty name and venue**
6. **Click "Add Course"**

### Managing Your Schedule

- **View course details**: Click on any occupied time slot
- **Remove courses**: Click on a course slot and press "Remove Course" 
- **Check conflicts**: The system automatically prevents conflicting course additions
- **Track progress**: View total enrolled courses and credits in the course list

### Understanding the Display

- **Blue slots**: Theory classes
- **Green slots**: Lab sessions  
- **Compact timing**: Each row shows both theory time and lab time
- **Course info**: Slots display course name and venue for clarity

## Technical Features

### Backend (Flask)
- **CSV Data Loading**: Automatically loads 160+ VIT courses from `courses.csv`
- **RESTful APIs**: Clean API endpoints for course management
- **Conflict Detection Engine**: Advanced algorithm to detect time overlaps
- **Multi-slot Processing**: Handles complex slot combinations

### Frontend (Vue.js + Bootstrap)
- **Reactive Interface**: Real-time updates using Vue.js 3
- **Responsive Design**: Bootstrap 5 for mobile-first design
- **Component Architecture**: Modular Vue components for maintainability
- **Search Integration**: Debounced search with dropdown results

### Data Management
- **In-memory Storage**: Fast timetable operations
- **CSV Integration**: Course database from VIT curriculum
- **Conflict Mapping**: Pre-computed conflict relationships between slots

## File Structure

```
FFCX/
├── app.py                 # Flask backend server
├── templates/
│   └── index.html        # Vue.js frontend application
├── courses.csv           # VIT course database (160+ courses)
├── tt.txt               # Reference timetable structure
├── requirements.txt      # Python dependencies
├── venv/                # Virtual environment (created during setup)
└── README.md            # This file
```

## API Endpoints

- `GET /` - Main application interface
- `GET /api/timetable` - Retrieve current timetable data
- `GET /api/courses` - Get enrolled courses with details
- `GET /api/search-courses?q={query}` - Search available courses
- `POST /api/add-course` - Add new course to timetable
- `POST /api/remove-course` - Remove course from timetable
- `GET /api/validate-slots` - Check for slot conflicts
- `GET /api/debug-conflicts` - Debug conflict detection (development)

## Course Data

The application includes comprehensive VIT course data:
- **160+ courses** from multiple departments (CSE, ECE, MATH, HUMANITIES, etc.)
- **Course codes, titles, types, and credits** from official VIT curriculum
- **Theory, Lab, and Embedded course types** properly categorized
- **Automatic metadata** extraction for course planning

## Conflict Detection

The system uses sophisticated conflict detection:
- **Time Overlap Analysis**: Checks actual time ranges (not just slot names)
- **Lab Session Handling**: Labs span multiple time periods and are properly validated
- **Cross-slot Conflicts**: Detects conflicts across different slot types
- **Multi-slot Validation**: Validates entire slot combinations before addition

## Future Enhancements

- [ ] **Database Integration**: PostgreSQL/MySQL for persistent storage
- [ ] **User Authentication**: Individual student accounts and profiles  
- [ ] **Collaborative Features**: Share timetables with friends
- [ ] **Export Options**: PDF/iCal export functionality
- [ ] **Mobile App**: Native iOS/Android applications
- [ ] **Faculty Integration**: Real faculty data and ratings
- [ ] **Semester Planning**: Multi-semester course planning
- [ ] **GPA Calculator**: Built-in GPA tracking and prediction

## Contributing

We welcome contributions from the VIT community! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes** and test thoroughly
4. **Submit a pull request** with detailed description

### Areas for Contribution
- UI/UX improvements and design enhancements
- Additional course data and validation
- Performance optimizations
- Mobile responsiveness improvements
- Test coverage and documentation

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact & Support

- **GitHub Issues**: Report bugs and request features
- **Repository**: [github.com/samarthnaikk/FFCX](https://github.com/samarthnaikk/FFCX)
- **Developer**: [@samarthnaikk](https://github.com/samarthnaikk)

---

**Made with ❤️ for VIT students by VIT students**
