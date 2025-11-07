# FFCX - Timetable Optimizer Setup Guide

## Prerequisites
- Node.js (v16 or higher)
- npm or yarn

## Installation

1. **Clone and install dependencies:**
   ```bash
   # Install root dependencies
   npm run install-all
   
   # Or manually install each:
   npm install
   cd server && npm install
   cd ../client && npm install
   ```

2. **Start the application:**
   ```bash
   # Start both frontend and backend together
   npm run dev
   
   # Or start them separately:
   # Backend only (runs on port 5000)
   npm run server
   
   # Frontend only (runs on port 3000)
   npm run client
   ```

## Project Structure

```
FFCX/
├── client/                 # React TypeScript frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── context/        # React context for state management
│   │   ├── services/       # API service layer
│   │   └── types/          # TypeScript type definitions
├── server/                 # Express.js backend
│   ├── models/            # Data models
│   ├── routes/            # API routes
│   ├── utils/             # Utility functions
│   └── server.js          # Main server file
├── data/                  # CSV data files
│   ├── courses.csv        # Course information
│   └── all_teachers.csv   # Teacher and slot information
└── package.json           # Root package.json for scripts
```

## API Endpoints

### Courses
- `GET /api/courses` - Get all courses or search
- `GET /api/courses/:courseCode` - Get specific course
- `GET /api/courses/search/autocomplete` - Autocomplete search

### Teachers
- `GET /api/teachers` - Get all teachers
- `GET /api/teachers/course/:courseCode` - Get teachers for a course
- `GET /api/teachers/faculty/:facultyName` - Get courses by faculty

### Timetable
- `GET /api/timetable` - Get current timetable
- `POST /api/timetable/add-course` - Add course to timetable
- `DELETE /api/timetable/remove-course/:courseId` - Remove course
- `POST /api/timetable/clear` - Clear timetable
- `POST /api/timetable/check-conflicts` - Check for conflicts

### Health Check
- `GET /api/health` - Server health check

## Features Implemented

✅ **Backend Features:**
- Express.js server with TypeScript-ready structure
- CSV data parsing and management
- Course and teacher data models
- RESTful API endpoints
- CORS and security middleware
- Error handling and logging

✅ **Frontend Features:**
- React TypeScript application
- Material-UI components
- Timetable grid visualization
- Course search with autocomplete
- Faculty and slot selection
- Conflict detection
- State management with React Context
- Responsive design

✅ **Data Management:**
- Course information from CSV
- Teacher and slot data integration
- VIT FFCS slot timing system
- Timetable conflict detection
- Export functionality

## Development Notes

- The application uses CSV files for data storage initially
- MongoDB integration ready for future development
- JWT authentication structure prepared
- Error handling and logging implemented
- TypeScript for type safety

## Next Steps for Production

1. **Database Integration:**
   - Replace CSV with MongoDB/PostgreSQL
   - Add data persistence
   - Implement user accounts

2. **Authentication:**
   - User registration/login
   - JWT token management
   - Role-based access control

3. **Advanced Features:**
   - Timetable optimization algorithms
   - Multiple timetable versions
   - Sharing and collaboration
   - Mobile responsiveness improvements

4. **Deployment:**
   - Docker containerization
   - Production environment setup
   - CI/CD pipeline
   - Performance optimization

## Troubleshooting

### Common Issues:

1. **Port conflicts:**
   - Backend runs on port 5000, Frontend on port 3000
   - Change ports in .env files if needed

2. **CORS issues:**
   - Ensure CLIENT_URL is set correctly in server/.env
   - Check that API_URL is correct in client/.env

3. **CSV data not loading:**
   - Verify CSV files exist in /data directory
   - Check file permissions
   - Look for parsing errors in server logs

### Quick Test:
```bash
# Test backend health
curl http://localhost:5000/api/health

# Test course data
curl http://localhost:5000/api/courses?limit=5
```