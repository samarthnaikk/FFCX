import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Button,
  TextField,
  Autocomplete,
  Paper,
  Typography,
  Collapse,
  useTheme,
  alpha,
} from '@mui/material';
import { Add as AddIcon, Close as CloseIcon } from '@mui/icons-material';
import { Course, mockCourses, searchCourses, getCoursesByFaculty } from '../services/courseService';

interface AddCourseFormProps {
  onAddCourse: (course: Course) => void;
}

const AddCourseForm: React.FC<AddCourseFormProps> = ({ onAddCourse }) => {
  const theme = useTheme();
  const [isOpen, setIsOpen] = useState(false);
  const [formData, setFormData] = useState<Partial<Course>>({
    courseCode: '',
    courseName: '',
    slot: '',
    venue: '',
    faculty: '',
    type: 'TH',
    curriculum: '',
    credits: 3
  });
  const [courseOptions, setCourseOptions] = useState<Course[]>([]);
  const [facultyOptions, setFacultyOptions] = useState<string[]>([]);

  // Available slots from the timetable
  const availableSlots = [
    'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'D1', 'D2', 'E1', 'E2', 'F1', 'F2', 'G1', 'G2',
    'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L31', 'L32', 'L33', 'L34', 'L35', 'L36'
  ];

  const venues = [
    'SJT101', 'SJT115', 'SJT118', 'SJT201', 'SJT215', 'PRP230', 'PRP734', 'PRP735',
    'TT631', 'SCOPE Lab1', 'SCOPE Lab2', 'ECE Lab', 'Mech Lab'
  ];

  useEffect(() => {
    // Get unique faculty names
    const facultySet = new Set(mockCourses.map(course => course.faculty));
    const faculties = Array.from(facultySet);
    setFacultyOptions(faculties);
  }, []);

  const handleCourseSearch = (query: string) => {
    const results = searchCourses(query);
    setCourseOptions(results);
  };

  const handleCourseSelect = (course: Course | null) => {
    if (course) {
      setFormData({
        ...course
      });
    }
  };

  const handleFacultySelect = (faculty: string | null) => {
    if (faculty) {
      const courses = getCoursesByFaculty(faculty);
      if (courses.length > 0) {
        const course = courses[0]; // Auto-fill with first course by this faculty
        setFormData({
          ...formData,
          faculty: faculty,
          venue: course.venue,
          type: course.type,
          curriculum: course.curriculum
        });
      } else {
        setFormData({
          ...formData,
          faculty: faculty
        });
      }
    }
  };

  const handleSubmit = () => {
    if (formData.courseCode && formData.courseName && formData.slot && formData.faculty) {
      onAddCourse(formData as Course);
      setFormData({
        courseCode: '',
        courseName: '',
        slot: '',
        venue: '',
        faculty: '',
        type: 'TH',
        curriculum: '',
        credits: 3
      });
      setIsOpen(false);
    }
  };

  const handleCancel = () => {
    setIsOpen(false);
    setFormData({
      courseCode: '',
      courseName: '',
      slot: '',
      venue: '',
      faculty: '',
      type: 'TH',
      curriculum: '',
      credits: 3
    });
  };

  return (
    <Box sx={{ mt: 2, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      {!isOpen && (
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setIsOpen(true)}
          sx={{
            backgroundColor: 'rgba(225, 29, 72, 0.8)',
            color: 'white',
            fontFamily: 'inherit',
            borderRadius: '12px',
            padding: '10px 24px',
            fontSize: '0.9rem',
            fontWeight: 'bold',
            '&:hover': {
              backgroundColor: 'rgba(225, 29, 72, 0.9)',
            },
            boxShadow: '0 4px 12px rgba(225, 29, 72, 0.3)',
          }}
        >
          Add Course
        </Button>
      )}

      <Collapse in={isOpen} timeout={300}>
        <Paper
          elevation={0}
          sx={{
            mt: 2,
            p: 3,
            borderRadius: '16px',
            backgroundColor: 'rgba(255, 255, 255, 0.1)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
            width: '600px',
            maxWidth: '90vw',
          }}
        >
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h6" sx={{ color: 'white', fontFamily: 'inherit', fontWeight: 'bold' }}>
              Add New Course
            </Typography>
            <Button
              onClick={handleCancel}
              sx={{ minWidth: 'auto', p: 1, color: 'rgba(255, 255, 255, 0.7)' }}
            >
              <CloseIcon />
            </Button>
          </Box>

          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Box sx={{ flex: 1, minWidth: '250px' }}>
                <Autocomplete
                  freeSolo
                  options={courseOptions}
                  getOptionLabel={(option) => typeof option === 'string' ? option : `${option.courseCode} - ${option.courseName}`}
                  onInputChange={(event, value) => handleCourseSearch(value)}
                  onChange={(event, value) => handleCourseSelect(typeof value === 'string' ? null : value)}
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      label="Course"
                      placeholder="Search by course code or name"
                      fullWidth
                      sx={{
                        '& .MuiOutlinedInput-root': {
                          backgroundColor: 'rgba(255, 255, 255, 0.1)',
                          color: 'white',
                          fontFamily: 'inherit',
                          '& fieldset': { borderColor: 'rgba(255, 255, 255, 0.3)' },
                          '&:hover fieldset': { borderColor: 'rgba(255, 255, 255, 0.5)' },
                          '&.Mui-focused fieldset': { borderColor: 'rgba(225, 29, 72, 0.8)' },
                        },
                        '& .MuiInputLabel-root': { color: 'rgba(255, 255, 255, 0.7)', fontFamily: 'inherit' },
                      }}
                    />
                  )}
                />
              </Box>
              <Box sx={{ flex: 1, minWidth: '200px' }}>
                <TextField
                  label="Course Code"
                  value={formData.courseCode || ''}
                  onChange={(e) => setFormData({ ...formData, courseCode: e.target.value })}
                  fullWidth
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                      color: 'white',
                      fontFamily: 'inherit',
                      '& fieldset': { borderColor: 'rgba(255, 255, 255, 0.3)' },
                      '&:hover fieldset': { borderColor: 'rgba(255, 255, 255, 0.5)' },
                      '&.Mui-focused fieldset': { borderColor: 'rgba(225, 29, 72, 0.8)' },
                    },
                    '& .MuiInputLabel-root': { color: 'rgba(255, 255, 255, 0.7)', fontFamily: 'inherit' },
                  }}
                />
              </Box>
            </Box>

            <TextField
              label="Course Name"
              value={formData.courseName || ''}
              onChange={(e) => setFormData({ ...formData, courseName: e.target.value })}
              fullWidth
              sx={{
                '& .MuiOutlinedInput-root': {
                  backgroundColor: 'rgba(255, 255, 255, 0.1)',
                  color: 'white',
                  fontFamily: 'inherit',
                  '& fieldset': { borderColor: 'rgba(255, 255, 255, 0.3)' },
                  '&:hover fieldset': { borderColor: 'rgba(255, 255, 255, 0.5)' },
                  '&.Mui-focused fieldset': { borderColor: 'rgba(225, 29, 72, 0.8)' },
                },
                '& .MuiInputLabel-root': { color: 'rgba(255, 255, 255, 0.7)', fontFamily: 'inherit' },
              }}
            />

            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Box sx={{ flex: 1, minWidth: '200px' }}>
                <Autocomplete
                  freeSolo
                  options={facultyOptions}
                  value={formData.faculty || ''}
                  onChange={(event, value) => handleFacultySelect(value)}
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      label="Faculty"
                      placeholder="Select or type faculty name"
                      fullWidth
                      sx={{
                        '& .MuiOutlinedInput-root': {
                          backgroundColor: 'rgba(255, 255, 255, 0.1)',
                          color: 'white',
                          fontFamily: 'inherit',
                          '& fieldset': { borderColor: 'rgba(255, 255, 255, 0.3)' },
                          '&:hover fieldset': { borderColor: 'rgba(255, 255, 255, 0.5)' },
                          '&.Mui-focused fieldset': { borderColor: 'rgba(225, 29, 72, 0.8)' },
                        },
                        '& .MuiInputLabel-root': { color: 'rgba(255, 255, 255, 0.7)', fontFamily: 'inherit' },
                      }}
                    />
                  )}
                />
              </Box>
              <Box sx={{ flex: 1, minWidth: '150px' }}>
                <Autocomplete
                  options={availableSlots}
                  value={formData.slot || ''}
                  onChange={(event, value) => setFormData({ ...formData, slot: value || '' })}
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      label="Slot"
                      placeholder="Select slot"
                      fullWidth
                      sx={{
                        '& .MuiOutlinedInput-root': {
                          backgroundColor: 'rgba(255, 255, 255, 0.1)',
                          color: 'white',
                          fontFamily: 'inherit',
                          '& fieldset': { borderColor: 'rgba(255, 255, 255, 0.3)' },
                          '&:hover fieldset': { borderColor: 'rgba(255, 255, 255, 0.5)' },
                          '&.Mui-focused fieldset': { borderColor: 'rgba(225, 29, 72, 0.8)' },
                        },
                        '& .MuiInputLabel-root': { color: 'rgba(255, 255, 255, 0.7)', fontFamily: 'inherit' },
                      }}
                    />
                  )}
                />
              </Box>
            </Box>

            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Box sx={{ flex: 1, minWidth: '200px' }}>
                <Autocomplete
                  freeSolo
                  options={venues}
                  value={formData.venue || ''}
                  onChange={(event, value) => setFormData({ ...formData, venue: value || '' })}
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      label="Venue"
                      placeholder="Select or type venue"
                      fullWidth
                      sx={{
                        '& .MuiOutlinedInput-root': {
                          backgroundColor: 'rgba(255, 255, 255, 0.1)',
                          color: 'white',
                          fontFamily: 'inherit',
                          '& fieldset': { borderColor: 'rgba(255, 255, 255, 0.3)' },
                          '&:hover fieldset': { borderColor: 'rgba(255, 255, 255, 0.5)' },
                          '&.Mui-focused fieldset': { borderColor: 'rgba(225, 29, 72, 0.8)' },
                        },
                        '& .MuiInputLabel-root': { color: 'rgba(255, 255, 255, 0.7)', fontFamily: 'inherit' },
                      }}
                    />
                  )}
                />
              </Box>
              <Box sx={{ flex: 0, minWidth: '120px' }}>
                <TextField
                  label="Credits"
                  type="number"
                  value={formData.credits || 3}
                  onChange={(e) => setFormData({ ...formData, credits: Number(e.target.value) })}
                  inputProps={{ min: 1, max: 6 }}
                  fullWidth
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                      color: 'white',
                      fontFamily: 'inherit',
                      '& fieldset': { borderColor: 'rgba(255, 255, 255, 0.3)' },
                      '&:hover fieldset': { borderColor: 'rgba(255, 255, 255, 0.5)' },
                      '&.Mui-focused fieldset': { borderColor: 'rgba(225, 29, 72, 0.8)' },
                    },
                    '& .MuiInputLabel-root': { color: 'rgba(255, 255, 255, 0.7)', fontFamily: 'inherit' },
                  }}
                />
              </Box>
            </Box>
          </Box>

          <Box sx={{ display: 'flex', gap: 2, mt: 3, justifyContent: 'flex-end' }}>
            <Button
              onClick={handleCancel}
              sx={{
                color: 'rgba(255, 255, 255, 0.7)',
                fontFamily: 'inherit',
                '&:hover': { backgroundColor: 'rgba(255, 255, 255, 0.1)' }
              }}
            >
              Cancel
            </Button>
            <Button
              onClick={handleSubmit}
              variant="contained"
              disabled={!formData.courseCode || !formData.courseName || !formData.slot || !formData.faculty}
              sx={{
                backgroundColor: 'rgba(225, 29, 72, 0.8)',
                color: 'white',
                fontFamily: 'inherit',
                '&:hover': { backgroundColor: 'rgba(225, 29, 72, 0.9)' },
                '&:disabled': { backgroundColor: 'rgba(255, 255, 255, 0.2)' }
              }}
            >
              Add Course
            </Button>
          </Box>
        </Paper>
      </Collapse>
    </Box>
  );
};

export default AddCourseForm;