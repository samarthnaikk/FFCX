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

// Theory hour timings from referencetext.txt
const THEORY_HOURS = [
  '8:00 AM to 8:50 AM', '9:00 AM to 9:50 AM', '10:00 AM to 10:50 AM', 
  '11:00 AM to 11:50 AM', '12:00 PM to 12:50 PM', '',
  '2:00 PM to 2:50 PM', '3:00 PM to 3:50 PM', '4:00 PM to 4:50 PM', 
  '5:00 PM to 5:50 PM', '6:00 PM to 6:50 PM', '6:51 PM to 7:00 PM', '7:01 PM to 7:50 PM'
];

// Lab hour timings from referencetext.txt
const LAB_HOURS = [
  '08:00 AM to 08:50 AM', '08:51 AM to 09:40 AM', '09:51 AM to 10:40 AM', 
  '10:41 AM to 11:30 AM', '11:40 AM to 12:30 PM', '12:31 PM to 1:20 PM', 'LUNCH',
  '2:00 PM to 2:50 PM', '2:51 PM to 3:40 PM', '3:51 PM to 4:40 PM', 
  '4:41 PM to 5:30 PM', '5:40 PM to 6:30 PM', '6:31 PM to 7:20 PM', ''
];

const DAYS = ['MON', 'TUE', 'WED', 'THU', 'FRI'];

// VIT FFCS day-wise slot mapping from referencetext.txt
const DAY_SLOT_MAPPING: { [day: string]: string[] } = {
  MON: ['A1 / L1', 'F1 / L2', 'D1 / L3', 'TB1 / L4', 'TG1 / L5', 'L6', '', 'A2 / L31', 'F2 / L32', 'D2 / L33', 'TB2 / L34', 'TG2 / L35', 'L36', 'V3'],
  TUE: ['B1 / L7', 'G1 / L8', 'E1 / L9', 'TC1 / L10', 'TAA1 / L11', 'L12', '', 'B2 / L37', 'G2 / L38', 'E2 / L39', 'TC2 / L40', 'TAA2 / L41', 'L42', 'V4'],
  WED: ['C1 / L13', 'A1 / L14', 'F1 / L15', 'V1 / L16', 'V2 / L17', 'L18', '', 'C2 / L43', 'A2 / L44', 'F2 / L45', 'TD2 / L46', 'TBB2 / L47', 'L48', 'V5'],
  THU: ['D1 / L19', 'B1 / L20', 'G1 / L21', 'TE1 / L22', 'TCC1 / L23', 'L24', '', 'D2 / L49', 'B2 / L50', 'G2 / L51', 'TE2 / L52', 'TCC2 / L53', 'L54', 'V6'],
  FRI: ['E1 / L25', 'C1 / L26', 'TA1 / L27', 'TF1 / L28', 'TD1 / L29', 'L30', '', 'E2 / L55', 'C2 / L56', 'TA2 / L57', 'TF2 / L58', 'TDD2 / L59', 'L60', 'V7']
};

// Sample timetable data for demonstration (can be populated with actual courses)
const SAMPLE_TIMETABLE: { [key: string]: any } = {
  // Add sample courses here if needed
  'A1': { courseCode: 'CSE2001', courseTitle: 'Computer Programming', faculty: 'Dr. Smith', venue: 'SJT101' },
  'B1': { courseCode: 'MAT2001', courseTitle: 'Calculus', faculty: 'Dr. Johnson', venue: 'SJT201' },
  'L1': { courseCode: 'CSE2001', courseTitle: 'Computer Programming Lab', faculty: 'Dr. Smith', venue: 'SCOPE Lab1' }
};

const TimetableGrid: React.FC = () => {
  const theme = useTheme();

  // Function to get course info for a slot
  const getCourseForSlot = (slotContent: string) => {
    if (!slotContent) return null;
    
    // Extract the main slot (first part before /)
    const mainSlot = slotContent.split(' / ')[0];
    return SAMPLE_TIMETABLE[mainSlot] || null;
  };

  // Function to render slot content
  const renderSlotContent = (slotContent: string) => {
    if (!slotContent || slotContent === '') {
      return (
        <Box sx={{ minHeight: 20 }}>
          <Typography variant="caption" color="textSecondary">
            -
          </Typography>
        </Box>
      );
    }

    const course = getCourseForSlot(slotContent);

    return (
      <Box
        sx={{
          backgroundColor: alpha(theme.palette.primary.main, 0.1),
          border: 1,
          borderColor: theme.palette.primary.main,
          borderRadius: 1,
          padding: 0.3,
          textAlign: 'center',
          minHeight: 20,
        }}
      >
        <Typography variant="caption" fontWeight="bold" display="block" sx={{ fontSize: '0.65rem' }}>
          {slotContent}
        </Typography>
        {course && (
          <Typography variant="caption" display="block" sx={{ fontSize: '0.55rem' }}>
            {course.courseCode}
          </Typography>
        )}
      </Box>
    );
  };

  return (
    <Box sx={{ width: '100%', height: '100vh', padding: 1, overflow: 'hidden' }}>
      <Typography variant="h6" fontWeight="bold" mb={1} textAlign="center">
        VIT FFCS Timetable
      </Typography>
      
      <TableContainer 
        component={Paper} 
        elevation={3}
        sx={{ 
          height: 'calc(100vh - 80px)',
          overflow: 'auto',
          fontSize: '0.7rem',
        }}
      >
        <Table size="small" sx={{ tableLayout: 'fixed' }}>
          {/* Theory Hours Row */}
          <TableHead>
            <TableRow sx={{ backgroundColor: alpha(theme.palette.primary.main, 0.1) }}>
              <TableCell 
                sx={{ 
                  backgroundColor: theme.palette.primary.main,
                  color: 'white',
                  fontWeight: 'bold',
                  width: '80px',
                  padding: 0.5,
                }}
              >
                <Typography variant="caption" fontWeight="bold">
                  THEORY HOURS
                </Typography>
              </TableCell>
              {THEORY_HOURS.map((time, index) => (
                <TableCell 
                  key={index}
                  align="center"
                  sx={{ 
                    backgroundColor: alpha(theme.palette.primary.main, 0.2),
                    fontWeight: 'bold',
                    width: '90px',
                    padding: 0.5,
                  }}
                >
                  <Typography variant="caption" fontWeight="bold" sx={{ fontSize: '0.6rem' }}>
                    {time || ''}
                  </Typography>
                </TableCell>
              ))}
            </TableRow>
          </TableHead>

          {/* Lab Hours Row */}
          <TableBody>
            <TableRow sx={{ backgroundColor: alpha(theme.palette.success.main, 0.1) }}>
              <TableCell 
                sx={{ 
                  backgroundColor: theme.palette.success.main,
                  color: 'white',
                  fontWeight: 'bold',
                  padding: 0.5,
                }}
              >
                <Typography variant="caption" fontWeight="bold">
                  LAB HOURS
                </Typography>
              </TableCell>
              {LAB_HOURS.map((time, index) => (
                <TableCell 
                  key={index}
                  align="center"
                  sx={{ 
                    backgroundColor: alpha(theme.palette.success.main, 0.2),
                    fontWeight: 'bold',
                    padding: 0.5,
                  }}
                >
                  <Typography variant="caption" fontWeight="bold" sx={{ fontSize: '0.6rem' }}>
                    {time === 'LUNCH' ? 'LUNCH' : time || ''}
                  </Typography>
                </TableCell>
              ))}
            </TableRow>

            {/* Days and Timetable Data */}
            {DAYS.map((day) => (
              <TableRow 
                key={day}
                sx={{ 
                  '&:nth-of-type(odd)': { 
                    backgroundColor: alpha(theme.palette.grey[50], 0.3) 
                  },
                  height: 60,
                }}
              >
                <TableCell 
                  sx={{ 
                    backgroundColor: alpha(theme.palette.info.main, 0.8),
                    color: 'white',
                    fontWeight: 'bold',
                    borderRight: `2px solid ${theme.palette.grey[300]}`,
                    padding: 1,
                  }}
                >
                  <Typography variant="body2" fontWeight="bold">
                    {day}
                  </Typography>
                </TableCell>
                {DAY_SLOT_MAPPING[day].map((slotContent, timeIndex) => (
                  <TableCell
                    key={`${day}-${timeIndex}`}
                    align="center"
                    sx={{
                      padding: 0.5,
                      verticalAlign: 'middle',
                    }}
                  >
                    {renderSlotContent(slotContent)}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default TimetableGrid;