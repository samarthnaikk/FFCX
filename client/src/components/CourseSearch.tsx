import React, { useState, useCallback, useEffect } from 'react';
import {
  Autocomplete,
  TextField,
  Box,
  Typography,
  Chip,
  Card,
  CardContent,
  Button,
  Stack,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
} from '@mui/material';
import { Add as AddIcon, Search as SearchIcon } from '@mui/icons-material';
import { courseApi, teacherApi } from '../services/api';
import { useTimetable } from '../context/TimetableContext';
import { AutocompleteOption, Course, FacultyGroup, Conflict } from '../types';

// Simple debounce function
function debounce<T extends (...args: any[]) => void>(
  func: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
}

const CourseSearch: React.FC = () => {
  const [courseOptions, setCourseOptions] = useState<AutocompleteOption[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<AutocompleteOption | null>(null);
  const [courseDetails, setCourseDetails] = useState<Course | null>(null);
  const [facultyGroups, setFacultyGroups] = useState<FacultyGroup[]>([]);
  const [selectedFaculty, setSelectedFaculty] = useState<string>('');
  const [selectedSlot, setSelectedSlot] = useState<string>('');
  const [loadingCourses, setLoadingCourses] = useState(false);
  const [loadingFaculty, setLoadingFaculty] = useState(false);
  const [conflicts, setConflicts] = useState<Conflict[]>([]);
  const [error, setError] = useState<string>('');

  const { addCourse, checkConflicts, loading: timetableLoading } = useTimetable();

  // Debounced course search
  const debouncedCourseSearch = useCallback(
    debounce(async (searchTerm: string) => {
      if (searchTerm.length < 2) {
        setCourseOptions([]);
        return;
      }

      setLoadingCourses(true);
      try {
        const options = await courseApi.getCoursesAutocomplete(searchTerm);
        setCourseOptions(options);
      } catch (error) {
        console.error('Failed to search courses:', error);
        setError('Failed to search courses');
      } finally {
        setLoadingCourses(false);
      }
    }, 300),
    []
  );

  // Handle course selection
  const handleCourseSelect = async (courseOption: AutocompleteOption | null) => {
    setSelectedCourse(courseOption);
    setSelectedFaculty('');
    setSelectedSlot('');
    setConflicts([]);
    setError('');
    
    if (!courseOption) {
      setCourseDetails(null);
      setFacultyGroups([]);
      return;
    }

    // Load course details
    try {
      const course = await courseApi.getCourse(courseOption.courseCode!);
      setCourseDetails(course);
    } catch (error) {
      console.error('Failed to load course details:', error);
    }

    // Load faculty options
    setLoadingFaculty(true);
    try {
      const faculty = await teacherApi.getTeachersByCourse(courseOption.courseCode!);
      setFacultyGroups(faculty);
    } catch (error) {
      console.error('Failed to load faculty:', error);
      setError('Failed to load faculty options');
    } finally {
      setLoadingFaculty(false);
    }
  };

  // Handle faculty selection
  const handleFacultySelect = (facultyName: string) => {
    setSelectedFaculty(facultyName);
    setSelectedSlot('');
    setConflicts([]);
  };

  // Handle slot selection and check conflicts
  const handleSlotSelect = async (slot: string) => {
    setSelectedSlot(slot);
    setConflicts([]);

    if (selectedCourse && selectedFaculty && slot) {
      try {
        const conflictList = await checkConflicts(
          selectedCourse.courseCode!,
          selectedFaculty,
          slot
        );
        setConflicts(conflictList);
      } catch (error) {
        console.error('Failed to check conflicts:', error);
      }
    }
  };

  // Add course to timetable
  const handleAddCourse = async () => {
    if (!selectedCourse || !selectedFaculty || !selectedSlot) {
      setError('Please select course, faculty, and slot');
      return;
    }

    const success = await addCourse(
      selectedCourse.courseCode!,
      selectedFaculty,
      selectedSlot
    );

    if (success) {
      // Reset form
      setSelectedCourse(null);
      setCourseDetails(null);
      setFacultyGroups([]);
      setSelectedFaculty('');
      setSelectedSlot('');
      setConflicts([]);
      setError('');
    }
  };

  // Get available slots for selected faculty
  const getAvailableSlots = () => {
    const facultyGroup = facultyGroups.find(fg => fg.faculty === selectedFaculty);
    return facultyGroup?.slots || [];
  };

  return (
    <Card elevation={3}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Add Course to Timetable
        </Typography>

        <Stack spacing={3}>
          {/* Course Search */}
            <Autocomplete
              options={courseOptions}
              value={selectedCourse}
              onChange={(_, value) => handleCourseSelect(value)}
              onInputChange={(_, value) => debouncedCourseSearch(value)}
              loading={loadingCourses}
              getOptionLabel={(option) => option.label}
              renderOption={(props, option) => (
                <Box component="li" {...props}>
                  <Box>
                    <Typography variant="body2" fontWeight="bold">
                      {option.courseCode}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      {option.courseTitle}
                    </Typography>
                    {option.credits && (
                      <Chip
                        label={`${option.credits} credits`}
                        size="small"
                        color="primary"
                        variant="outlined"
                        sx={{ ml: 1 }}
                      />
                    )}
                  </Box>
                </Box>
              )}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Search Course"
                  placeholder="Type course code or title..."
                  InputProps={{
                    ...params.InputProps,
                    startAdornment: <SearchIcon color="action" sx={{ mr: 1 }} />,
                    endAdornment: (
                      <>
                        {loadingCourses ? <CircularProgress size={20} /> : null}
                        {params.InputProps.endAdornment}
                      </>
                    ),
                  }}
                />
              )}
              noOptionsText="No courses found"
            />
          </Grid>

          {/* Course Details */}
          {courseDetails && (
            <Grid item xs={12}>
              <Box sx={{ p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Course Details
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Typography variant="body2">
                      <strong>Type:</strong> {courseDetails.courseType}
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2">
                      <strong>Credits:</strong> {courseDetails.credits}
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2">
                      <strong>Total Hours:</strong> {courseDetails.totalHours}
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2">
                      <strong>L-T-P-J:</strong> {courseDetails.lectureHours}-{courseDetails.tutorialHours}-{courseDetails.practicalHours}-{courseDetails.projectHours}
                    </Typography>
                  </Grid>
                </Grid>
              </Box>
            </Grid>
          )}

          {/* Faculty Selection */}
          {facultyGroups.length > 0 && (
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Select Faculty</InputLabel>
                <Select
                  value={selectedFaculty}
                  onChange={(e) => handleFacultySelect(e.target.value)}
                  label="Select Faculty"
                  disabled={loadingFaculty}
                >
                  {facultyGroups.map((facultyGroup) => (
                    <MenuItem key={facultyGroup.faculty} value={facultyGroup.faculty}>
                      <Box>
                        <Typography variant="body2">{facultyGroup.faculty}</Typography>
                        <Typography variant="caption" color="textSecondary">
                          {facultyGroup.slots.length} slot{facultyGroup.slots.length > 1 ? 's' : ''} available
                        </Typography>
                      </Box>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          )}

          {/* Slot Selection */}
          {selectedFaculty && getAvailableSlots().length > 0 && (
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Select Slot</InputLabel>
                <Select
                  value={selectedSlot}
                  onChange={(e) => handleSlotSelect(e.target.value)}
                  label="Select Slot"
                >
                  {getAvailableSlots().map((slotInfo) => (
                    <MenuItem key={slotInfo.slot} value={slotInfo.slot}>
                      <Box>
                        <Typography variant="body2">{slotInfo.slot}</Typography>
                        <Typography variant="caption" color="textSecondary">
                          {slotInfo.venue} • {slotInfo.type}
                        </Typography>
                      </Box>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          )}

          {/* Conflicts Display */}
          {conflicts.length > 0 && (
            <Grid item xs={12}>
              <Alert severity="warning">
                <Typography variant="subtitle2" gutterBottom>
                  Slot Conflicts Detected:
                </Typography>
                {conflicts.map((conflict, index) => (
                  <Typography key={index} variant="body2">
                    • {conflict.message}
                  </Typography>
                ))}
              </Alert>
            </Grid>
          )}

          {/* Error Display */}
          {error && (
            <Grid item xs={12}>
              <Alert severity="error">{error}</Alert>
            </Grid>
          )}

          {/* Add Button */}
          <Grid item xs={12}>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={handleAddCourse}
              disabled={
                !selectedCourse || 
                !selectedFaculty || 
                !selectedSlot || 
                conflicts.length > 0 || 
                timetableLoading
              }
              fullWidth
              size="large"
            >
              {timetableLoading ? 'Adding...' : 'Add Course to Timetable'}
            </Button>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default CourseSearch;