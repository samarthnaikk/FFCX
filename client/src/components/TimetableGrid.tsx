import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Box,
  useTheme,
  alpha,
} from '@mui/material';

// Time slot definitions based on VIT FFCS
const TIME_SLOTS = [
  { slot: 'A1/B1/C1/D1/E1', time: '08:00 - 08:50' },
  { slot: 'A2/B2/C2/D2/E2', time: '09:00 - 09:50' },
  { slot: 'F1/F2/G1/G2', time: '10:00 - 10:50' },
  { slot: 'TAA1/TBB1/TCC1/TDD1/TEE1', time: '11:00 - 11:50' },
  { slot: 'TAA2/TBB2/TCC2/TDD2/TEE2', time: '12:00 - 12:50' },
  { slot: 'L1/L2/L3/L4/L5', time: '14:00 - 16:50' },
  { slot: 'L6/L7/L8/L9/L10', time: '17:00 - 19:50' },
];

const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

// Sample timetable data for demonstration
const SAMPLE_TIMETABLE: { [day: string]: { [slot: string]: any[] } } = {
  Monday: {
    'A1': [{
      courseCode: 'CSE101',
      courseTitle: 'Programming Fundamentals',
      faculty: 'Dr. Smith',
      venue: 'SJT101',
      type: 'TH',
      credits: 3
    }]
  },
  Tuesday: {
    'A2': [{
      courseCode: 'MAT101',
      courseTitle: 'Calculus',
      faculty: 'Dr. Johnson',
      venue: 'SJT201',
      type: 'TH',
      credits: 4
    }]
  },
  Wednesday: {},
  Thursday: {},
  Friday: {}
};

const TimetableGrid: React.FC = () => {
  const theme = useTheme();

  // Function to get entries for a specific day and time slot
  const getEntriesForSlot = (day: string, timeSlot: string): any[] => {
    const daySchedule = SAMPLE_TIMETABLE[day] || {};
    const entries: any[] = [];

    // Check all possible slots for this time period
    const slotsToCheck = timeSlot.split('/');
    slotsToCheck.forEach(slot => {
      if (daySchedule[slot]) {
        entries.push(...daySchedule[slot]);
      }
    });

    return entries;
  };

  // Function to get color based on course type
  const getCourseColor = (type: string, isLab: boolean = false) => {
    if (isLab || type === 'LAB') {
      return {
        backgroundColor: alpha(theme.palette.success.main, 0.1),
        borderColor: theme.palette.success.main,
        color: theme.palette.success.dark,
      };
    }
    return {
      backgroundColor: alpha(theme.palette.primary.main, 0.1),
      borderColor: theme.palette.primary.main,
      color: theme.palette.primary.dark,
    };
  };

  // Render course entry
  const renderCourseEntry = (entry: any, index: number) => {
    const isLab = entry.type === 'LAB';
    const colors = getCourseColor(entry.type, isLab);

    return (
      <Box
        key={index}
        sx={{
          ...colors,
          border: 1,
          borderRadius: 1,
          padding: 1,
          margin: 0.25,
          textAlign: 'center',
          minHeight: 40,
        }}
      >
        <Typography variant="caption" fontWeight="bold" display="block">
          {entry.courseCode}
        </Typography>
        <Typography variant="caption" display="block">
          {entry.faculty}
        </Typography>
      </Box>
    );
  };

  return (
    <TableContainer 
      component={Paper} 
      elevation={3}
      sx={{ 
        maxHeight: '70vh',
        overflow: 'auto',
      }}
    >
      <Table stickyHeader>
        <TableHead>
          <TableRow>
            <TableCell 
              sx={{ 
                backgroundColor: theme.palette.grey[100],
                fontWeight: 'bold',
                minWidth: 120,
              }}
            >
              <Typography variant="subtitle1" fontWeight="bold">
                Time / Day
              </Typography>
            </TableCell>
            {DAYS.map((day) => (
              <TableCell 
                key={day}
                align="center"
                sx={{ 
                  backgroundColor: theme.palette.grey[100],
                  fontWeight: 'bold',
                  minWidth: 180,
                }}
              >
                <Typography variant="subtitle1" fontWeight="bold">
                  {day}
                </Typography>
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {TIME_SLOTS.map((timeSlot) => (
            <TableRow 
              key={timeSlot.slot}
              sx={{ 
                '&:nth-of-type(odd)': { 
                  backgroundColor: alpha(theme.palette.grey[50], 0.5) 
                },
                height: 80,
              }}
            >
              <TableCell 
                sx={{ 
                  backgroundColor: alpha(theme.palette.grey[100], 0.7),
                  borderRight: `2px solid ${theme.palette.grey[300]}`,
                }}
              >
                <Typography variant="body2" fontWeight="medium">
                  {timeSlot.time}
                </Typography>
                <Typography variant="caption" color="textSecondary">
                  {timeSlot.slot}
                </Typography>
              </TableCell>
              {DAYS.map((day) => {
                const entries = getEntriesForSlot(day, timeSlot.slot);
                return (
                  <TableCell
                    key={`${day}-${timeSlot.slot}`}
                    align="center"
                    sx={{
                      padding: 1,
                      verticalAlign: 'top',
                    }}
                  >
                    {entries.length > 0 ? (
                      <Box>
                        {entries.map((entry, index) => renderCourseEntry(entry, index))}
                      </Box>
                    ) : (
                      <Typography variant="caption" color="textSecondary">
                        Free
                      </Typography>
                    )}
                  </TableCell>
                );
              })}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default TimetableGrid;