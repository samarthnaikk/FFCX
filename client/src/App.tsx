import React, { useState } from 'react';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  Container,
  AppBar,
  Toolbar,
  Typography,
  Box,
  Button,
  Stack,
  Paper,
  Alert,
  Chip,
} from '@mui/material';
import {
  Schedule as ScheduleIcon,
  Add as AddIcon,
  Clear as ClearIcon,
  Download as DownloadIcon,
} from '@mui/icons-material';
import { TimetableProvider, useTimetable } from './context/TimetableContext';
import TimetableGrid from './components/TimetableGrid';
import CourseSearchSimple from './components/CourseSearchSimple';
import { TimetableEntry } from './types';
import './App.css';

// Create MUI theme
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    h4: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 500,
    },
  },
});

// Main App Content Component
const AppContent: React.FC = () => {
  const { timetable, loading, error, clearTimetable } = useTimetable();
  const [selectedSlotInfo, setSelectedSlotInfo] = useState<{
    day: string;
    slot: string;
    entries: TimetableEntry[];
  } | null>(null);

  const handleSlotClick = (day: string, slot: string, entries: TimetableEntry[]) => {
    setSelectedSlotInfo({ day, slot, entries });
  };

  const handleClearTimetable = async () => {
    if (window.confirm('Are you sure you want to clear the entire timetable?')) {
      await clearTimetable();
    }
  };

  const handleExportTimetable = () => {
    if (!timetable) return;
    
    const dataStr = JSON.stringify(timetable, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `ffcx-timetable-${new Date().toISOString().split('T')[0]}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* App Bar */}
      <AppBar position="static" elevation={2}>
        <Toolbar>
          <ScheduleIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            FFCX - Timetable Optimizer
          </Typography>
          <Button
            color="inherit"
            startIcon={<DownloadIcon />}
            onClick={handleExportTimetable}
            disabled={!timetable || timetable.totalCourses === 0}
          >
            Export
          </Button>
          <Button
            color="inherit"
            startIcon={<ClearIcon />}
            onClick={handleClearTimetable}
            disabled={loading || !timetable || timetable.totalCourses === 0}
          >
            Clear All
          </Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 3, mb: 3 }}>
        {/* Error Display */}
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {/* Timetable Summary */}
        {timetable && (
          <Paper elevation={2} sx={{ p: 2, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Timetable Summary
            </Typography>
            <Stack direction="row" spacing={2}>
              <Chip
                label={`${timetable.totalCourses} Courses`}
                color="primary"
                variant="outlined"
              />
              <Chip
                label={`${timetable.totalCredits} Credits`}
                color="secondary"
                variant="outlined"
              />
              {timetable.conflicts.length > 0 && (
                <Chip
                  label={`${timetable.conflicts.length} Conflicts`}
                  color="error"
                />
              )}
            </Stack>
          </Paper>
        )}

        <Stack spacing={3}>
          {/* Course Search Section */}
          <CourseSearchSimple />

          {/* Timetable Grid Section */}
          <Paper elevation={2} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Weekly Timetable
            </Typography>
            <TimetableGrid onSlotClick={handleSlotClick} />
          </Paper>

          {/* Selected Slot Details */}
          {selectedSlotInfo && (
            <Paper elevation={2} sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                {selectedSlotInfo.day} - {selectedSlotInfo.slot}
              </Typography>
              <Stack spacing={2}>
                {selectedSlotInfo.entries.map((entry, index) => (
                  <Box
                    key={index}
                    sx={{
                      p: 2,
                      border: 1,
                      borderColor: 'divider',
                      borderRadius: 1,
                      bgcolor: 'grey.50',
                    }}
                  >
                    <Typography variant="subtitle1" fontWeight="bold">
                      {entry.courseCode} - {entry.courseTitle}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Faculty: {entry.faculty}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Venue: {entry.venue}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Type: {entry.type} • Credits: {entry.credits} • Time: {entry.time}
                    </Typography>
                  </Box>
                ))}
              </Stack>
            </Paper>
          )}
        </Stack>
      </Container>
    </Box>
  );
};

// Main App Component with Provider
function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <TimetableProvider>
        <AppContent />
      </TimetableProvider>
    </ThemeProvider>
  );
}

export default App;
