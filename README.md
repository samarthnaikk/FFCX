# FFCX - Advanced FFCS Timetable Optimizer for VIT Students


## Overview

FFCX is a comprehensive web application designed to help VIT (Vellore Institute of Technology) students create, optimize, and manage their FFCS (Fully Flexible Credit System) timetables. This platform provides an intuitive interface for course selection, teacher preference management, intelligent timetable optimization, and advanced conflict detection based on actual VIT FFCS slot timings.

**Quick Start**: Visit [ffcx.vercel.app](https://ffcx.vercel.app) to start planning your timetable immediately!

## What is FFCS?

The Fully Flexible Credit System (FFCS) is VIT's unique academic structure that allows students to:
- Choose their own courses based on interest and career goals
- Select preferred faculty members and class timings
- Create flexible timetables with theory and lab components
- Progress at their own pace across different semesters

## Key Features

### NEW: AI-Powered Timetable Optimization
- **Teacher Preference Management**: Set multiple teacher options for each course with priority rankings
- **Subject Priority System**: Assign priority levels to courses (1 = highest priority)
- **Intelligent Assignment**: Automatically generates optimal timetables based on your preferences
- **Conflict Resolution**: Identifies and explains why certain assignments fail
- **Comprehensive Feedback**: Detailed reports on successful assignments, failures, and conflicts

### Interactive Timetable Management
- **Visual Timetable Display**: Clean, responsive grid showing Monday-Friday schedule
- **Theory vs Lab Distinction**: Different color coding for theory (blue) and lab (green) sessions
- **Accurate Timing**: Based on actual VIT FFCS slot timings with proper lab hour calculations
- **Click-to-View Details**: Click any occupied slot to see course details
- **Real-time Updates**: Instant visual feedback when making changes

### Smart Course Search & Discovery
- **Autocomplete Search**: Type to search from 160+ VIT courses loaded from CSV database
- **Auto-fill Information**: Selecting a course automatically fills course code, type, and credits
- **Editable Fields**: All auto-filled fields remain editable for customization
- **Integrated Search**: Consistent search experience across add course and preferences

### Advanced Slot & Preference Management
- **Multi-Slot Support**: Add courses with multiple slots (e.g., A1+L5 for theory+lab combinations)
- **Teacher Options**: Configure multiple teacher choices per course with priority rankings
- **Priority-Based Selection**: Lower priority numbers indicate higher importance (1 = highest)
- **Flexible Course Assignment**: Add courses and teachers independently through preferences
- **Venue Management**: Specify preferred venues for each teacher option

### Intelligent Optimization Engine
- **Greedy Scheduling Algorithm**: Optimizes timetable based on course and teacher priorities
- **Conflict Avoidance**: Automatically prevents slot conflicts during optimization
- **Comprehensive Reporting**: Detailed success/failure reports with explanations
- **Multiple Teacher Options**: Tries teacher options in priority order until successful assignment
- **Slot Availability Checking**: Validates all slot requirements before assignment

### Advanced Conflict Detection & Validation
- **Slot Conflict Prevention**: Prevents adding courses that conflict with existing schedule
- **Multi-slot Validation**: Validates entire slot combinations before adding
- **Lab-Theory Overlap Detection**: Prevents conflicts between lab sessions and overlapping theory classes
- **Post-Optimization Clash Detection**: Automatically checks for conflicts after optimization
- **Real-time Feedback**: Immediate validation with detailed conflict explanations

### Comprehensive Course Management
- **Add/Remove Courses**: Easy course addition with comprehensive form validation
- **Course List Display**: View all enrolled courses with credits, faculty, and venue information
- **Dynamic Statistics**: Real-time calculation of total credits from enrolled courses
- **Preference Storage**: Persistent storage of teacher preferences in browser
- **Export/Import Options**: Save and restore timetable configurations

### User Experience
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Bootstrap 5 Styling**: Modern, professional interface
- **Vue.js Interactivity**: Real-time updates without page refreshes
- **Intuitive Icons**: Clear visual indicators for different course types

## Getting Started

### Option 1: Use the Live Application (Recommended)

**The easiest way to get started is to use our hosted version:**

**[Visit FFCX Live Application](https://ffcx.vercel.app)**

- **No installation required**
- **Always up-to-date**
- **Works on any device with a web browser**
- **Instant access to all features**

### Option 2: Local Development Setup

For developers who want to run FFCX locally or contribute to the project:

#### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

#### Installation

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

#### Running the Application Locally

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

> **Tip**: For regular use, we recommend using the [live hosted version](https://ffcx.vercel.app) instead of local setup.

## How to Use

### Quick Start: Optimize Your Timetable

1. **Click the "Preferences" button** next to the "+" button
2. **Add your preferred courses**:
   - Search and select courses using the autocomplete dropdown
   - Set course priority (1 = highest priority, 10 = lowest)
3. **Configure teacher options** for each course:
   - Add multiple teachers with their slots, venues, and priorities
   - Lower priority numbers = higher preference (1 = most preferred)
4. **Click "Optimize Timetable"** to automatically generate your schedule
5. **Review results**: See successful assignments, failed courses, and any conflicts

### Manual Course Addition

1. **Click the "+" button** next to "Enrolled Courses"
2. **Search for courses** by typing in the course name field (e.g., type "data" to see Data Structures, Data Mining, etc.)
3. **Select from dropdown** to auto-fill course code, type, and credits
4. **Enter slot information**:
   - Single slot: `A1`, `B2`, `L31`
   - Multiple slots: `A1+L5`, `B1+B2`, `C1+L15+L16`
5. **Add faculty name and venue**
6. **Click "Add Course"**

### Teacher Preference Management

1. **Access Preferences**: Click the "Preferences" button
2. **Add Courses**: Search and add courses you're interested in
3. **Configure Teachers**: For each course, add multiple teacher options:
   - Teacher name and slot combinations
   - Venue preferences
   - Priority ranking (1-10, where 1 = highest priority)
4. **Set Course Priorities**: Assign overall priority to each course
5. **Optimize**: Let the algorithm find the best combination

### Managing Your Schedule

- **View course details**: Click on any occupied time slot
- **Remove courses**: Click on a course slot and press "Remove Course" 
- **Check conflicts**: The system automatically prevents conflicting course additions
- **Track progress**: View total enrolled courses and credits in the course list
- **Optimize anytime**: Use preferences to regenerate optimal schedules

### Understanding the Display

- **Blue slots**: Theory classes
- **Green slots**: Lab sessions  
- **Compact timing**: Each row shows both theory time and lab time
- **Course info**: Slots display course name and venue for clarity

## Technical Architecture

### Backend (Flask + Python)
- **RESTful API Design**: Clean, documented endpoints for all operations
- **CSV Data Integration**: Automatically loads 160+ VIT courses from `courses.csv`
- **Advanced Optimization Engine**: Greedy scheduling algorithm with priority-based assignment
- **Conflict Detection System**: Pre-computed conflict mapping with time overlap analysis
- **Multi-slot Processing**: Handles complex slot combinations and assignments
- **Comprehensive Validation**: Server-side validation for all course operations

### Frontend (Vue.js 3 + Bootstrap 5)
- **Reactive Architecture**: Real-time updates using Vue.js 3 Composition API
- **Responsive Design**: Mobile-first Bootstrap 5 implementation
- **Component-Based Structure**: Modular Vue components for maintainability
- **Advanced Search Integration**: Debounced search with autocomplete dropdowns
- **Local Storage Persistence**: Browser-based preference storage
- **Modern UI/UX**: Professional interface with Font Awesome icons

### Data Management & Algorithms
- **In-Memory Timetable Storage**: Fast operations with structured data models
- **Priority Queue Processing**: Efficient course assignment based on priorities
- **Conflict Resolution Engine**: Sophisticated overlap detection and prevention
- **Preference Persistence**: Client-side storage with JSON serialization
- **Real-time Validation**: Immediate feedback on user actions

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

### Core Timetable Operations
- `GET /` - Main application interface
- `GET /api/timetable` - Retrieve current timetable data
- `GET /api/courses` - Get enrolled courses with details
- `POST /api/add-course` - Add new course to timetable
- `POST /api/remove-course` - Remove course from timetable

### Search & Discovery
- `GET /api/search-courses?q={query}` - Search available courses with autocomplete
- `GET /api/available-courses` - Get all available courses from database

### Optimization & Preferences
- `POST /api/optimize-timetable` - **NEW**: Optimize timetable based on preferences
- `GET /api/validate-slots` - Check for slot conflicts in current timetable

### Import/Export & Utilities
- `GET /api/export-timetable` - Export current timetable configuration
- `POST /api/import-timetable` - Import timetable from saved configuration
- `GET /api/slot-info` - Get detailed slot timing and availability information
- `GET /api/debug-conflicts` - Debug conflict detection (development mode)

## Advanced Features

### Timetable Optimization Algorithm
The optimization engine uses a sophisticated greedy scheduling approach:

1. **Priority-Based Processing**: Courses are processed in priority order (1 = highest)
2. **Teacher Option Evaluation**: For each course, teacher options are tried in priority order
3. **Conflict Avoidance**: Real-time slot conflict detection during assignment
4. **Comprehensive Validation**: All slot requirements validated before assignment
5. **Detailed Reporting**: Success/failure feedback with specific reasons

### Conflict Detection System
- **Time Overlap Analysis**: Checks actual time ranges (not just slot names)
- **Lab Session Handling**: Labs span multiple time periods and are properly validated
- **Cross-slot Conflicts**: Detects conflicts across different slot types
- **Multi-slot Validation**: Validates entire slot combinations before addition
- **Real-time Feedback**: Immediate validation with detailed explanations

### Course Database Integration
The application includes comprehensive VIT course data:
- **160+ courses** from multiple departments (CSE, ECE, MATH, HUMANITIES, etc.)
- **Course codes, titles, types, and credits** from official VIT curriculum
- **Theory, Lab, and Embedded course types** properly categorized
- **Automatic metadata** extraction for course planning

## Future Enhancements

### Planned Features
- [ ] **Machine Learning Integration**: AI-powered course recommendations based on academic history
- [ ] **Database Migration**: PostgreSQL/MySQL for persistent storage and scalability
- [ ] **User Authentication**: Individual student accounts with secure login
- [ ] **Collaborative Planning**: Share and collaborate on timetables with friends
- [ ] **Advanced Analytics**: GPA prediction and academic performance insights
- [ ] **Real Faculty Integration**: Live faculty data, ratings, and availability

### Export & Integration
- [ ] **Multiple Export Formats**: PDF, iCal, Google Calendar integration
- [ ] **Mobile Applications**: Native iOS/Android apps with offline support
- [ ] **VIT Portal Integration**: Direct integration with official VIT systems
- [ ] **Notification System**: Reminders for course registration periods

### Enhanced Optimization
- [ ] **Multi-Semester Planning**: Plan entire academic year with course prerequisites
- [ ] **Load Balancing**: Optimize for even distribution of daily workload
- [ ] **Custom Constraints**: Add personal preferences (no morning classes, etc.)
- [ ] **Alternative Solutions**: Generate multiple optimal timetable options

## Contributing

We welcome contributions from the VIT community! FFCX is built by students, for students.

### How to Contribute

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** and test thoroughly
4. **Follow code standards**: Maintain existing code style and documentation
5. **Submit a pull request** with detailed description of changes

### Priority Areas for Contribution

#### Frontend Development
- UI/UX improvements and modern design enhancements
- Mobile responsiveness and touch interface optimization
- Accessibility improvements (WCAG compliance)
- Performance optimizations and lazy loading

#### Backend Development
- Database integration and migration scripts
- API optimization and caching strategies
- Advanced algorithms for timetable optimization
- Integration with external VIT systems

#### Data & Content
- Course database updates and validation
- Faculty information and rating systems
- Academic calendar integration
- Department-specific customizations

#### Testing & Documentation
- Comprehensive test coverage (unit, integration, e2e)
- API documentation and examples
- User guides and tutorials
- Performance benchmarking

### Development Setup

1. Follow the installation instructions above
2. Enable debug mode in `app.py`
3. Use browser developer tools for frontend debugging
4. Check console logs for optimization algorithm details

### Code Standards
- **Python**: Follow PEP 8 style guidelines
- **JavaScript**: Use ES6+ features and Vue.js best practices
- **HTML/CSS**: Semantic markup and responsive design principles
- **Documentation**: Clear comments and README updates

## License & Legal

This project is open source and available under the [MIT License](LICENSE).

### Disclaimer
- This application is an independent student project and is not officially affiliated with VIT
- Course data is collected from publicly available sources and may not reflect real-time changes
- Users should verify all course information with official VIT sources before registration
- The developers are not responsible for any academic or administrative issues arising from using this tool

## Contact & Support

### Getting Help
- **GitHub Issues**: [Report bugs and request features](https://github.com/samarthnaikk/FFCX/issues)
- **Discussions**: [Community discussions and questions](https://github.com/samarthnaikk/FFCX/discussions)
- **Documentation**: Check this README and inline code documentation

### Connect with the Team
- **Repository**: [github.com/samarthnaikk/FFCX](https://github.com/samarthnaikk/FFCX)
- **Developer**: [@samarthnaikk](https://github.com/samarthnaikk)
- **Stars**: If you find this helpful, please star the repository!

### Stay Updated
- **Watch** the repository for updates and new releases
- **Follow** the project for announcements
- **Contribute** to help improve the platform for all VIT students

</div>
