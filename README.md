# VIT FFCS Timetable System

A simple HTML/CSS/JavaScript timetable system with Python Flask backend for VIT's Fully Flexible Credit System (FFCS).

## Features

- **Glassmorphism Design**: Mac-style black background with glass effects and rose red accents
- **CSV Data Integration**: Loads course and faculty data from CSV files
- **Interactive Timetable**: Displays VIT FFCS slot structure with theory and lab hours
- **Add Course Functionality**: Search and add courses with auto-complete
- **Faculty Search**: Auto-fill course details based on faculty selection

## Project Structure

```
FFCX/
├── index.html          # Main timetable interface
├── styles.css          # Glassmorphism styling
├── script.js           # Frontend JavaScript logic
├── server.py           # Python Flask backend
├── requirements.txt    # Python dependencies
├── data/
│   ├── courses.csv     # Course information (codes, credits, etc.)
│   └── all_teachers.csv # Faculty assignments (slots, venues, etc.)
└── README.md
```

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Python Server

```bash
python server.py
```

The server will start at `http://localhost:5000`

### 3. Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## CSV Data Format

### courses.csv
```csv
Course Code,Course Title,Course Type,Version,L,T,P,J,Credits
BCHY101L,Engineering Chemistry,Theory,1,3,0,0,0,3
```

### all_teachers.csv
```csv
Curriculum,Course Code,Course Name,Slot,Venue,Faculty,Type
FC - Foundation Core,BCHY101L,Engineering Chemistry,C2,PRP735,SATHISH KUMAR P,TH
```

## API Endpoints

- `GET /api/courses` - Get all courses and faculty data
- `GET /api/search?q=<query>` - Search courses by name, code, or faculty
- `GET /api/faculty` - Get list of all faculty members
- `GET /api/faculty/<name>` - Get courses taught by specific faculty

## Usage

1. **View Timetable**: The main page displays the VIT FFCS timetable grid with time slots
2. **Add Course**: Click "Add Course" button to open the course addition form
3. **Search Courses**: Type in the course search field to find courses by code, name, or faculty
4. **Auto-fill**: Select a faculty member to auto-fill venue and course type information
5. **Submit**: Fill required fields and submit to add the course to your timetable

## Design Features

- **Font**: Elms Sans typography for clean, modern appearance
- **Background**: Pure black (#000000) for Mac-style aesthetics
- **Glass Effects**: Backdrop blur with semi-transparent elements
- **Accent Color**: Rose red (#E11D48) for highlights and interactive elements
- **Responsive**: Adapts to different screen sizes

## Development Notes

This application was converted from a React TypeScript project to vanilla HTML/CSS/JavaScript with Python backend for simplicity and easier deployment.