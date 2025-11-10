import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
  Box,
  useTheme,
  alpha,
} from '@mui/material';

// Theory hour timings from referencetext.txt
const THEORY_HOURS = [
  '8:00 AM to 8:50 AM', '9:00 AM to 9:50 AM', '10:00 AM to 10:50 AM', 
  '11:00 AM to 11:50 AM', '12:00 PM to 12:50 PM', '', '',
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

const TimetableGrid: React.FC = () => {
  const theme = useTheme();

  // Function to format time range (start time above end time)
  const formatTimeRange = (timeRange: string) => {
    if (!timeRange || timeRange === '' || timeRange === 'LUNCH') {
      return timeRange;
    }
    
    const [startTime, endTime] = timeRange.split(' to ');
    return { startTime, endTime };
  };

  // Function to render time cell content
  const renderTimeCell = (timeRange: string) => {
    if (timeRange === 'LUNCH') {
      return (
        <Box sx={{
          backgroundColor: 'rgba(255, 255, 255, 0.15)',
          padding: '6px 8px',
          borderRadius: 1,
          display: 'inline-block',
          border: '1px solid rgba(255, 255, 255, 0.2)',
        }}>
          <Typography variant="body2" fontWeight="bold" sx={{ fontSize: '0.95rem', color: '#ffffff', fontFamily: 'inherit' }}>
            LUNCH
          </Typography>
        </Box>
      );
    }

    if (!timeRange || timeRange === '') {
      return null;
    }

    const timeObj = formatTimeRange(timeRange);
    if (typeof timeObj === 'object' && timeObj.startTime && timeObj.endTime) {
      return (
        <Box sx={{ textAlign: 'center' }}>
          <Typography variant="body2" fontWeight="bold" sx={{ fontSize: '0.85rem', lineHeight: 1.1, color: '#ffffff', fontFamily: 'inherit' }}>
            {timeObj.startTime}
          </Typography>
          <Typography variant="caption" sx={{ fontSize: '0.7rem', lineHeight: 1, color: 'rgba(255, 255, 255, 0.7)', fontFamily: 'inherit' }}>
            to
          </Typography>
          <Typography variant="body2" fontWeight="bold" sx={{ fontSize: '0.85rem', lineHeight: 1.1, color: '#ffffff', fontFamily: 'inherit' }}>
            {timeObj.endTime}
          </Typography>
        </Box>
      );
    }

    return (
      <Typography variant="body2" fontWeight="bold" sx={{ fontSize: '0.75rem' }}>
        {timeRange}
      </Typography>
    );
  };

  // Function to render slot content
  const renderSlotContent = (slotContent: string) => {
    if (!slotContent || slotContent === '') {
      return (
        <Box sx={{ 
          minHeight: 40, 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          width: '100%'
        }}>
          <Typography variant="body2" color="rgba(255, 255, 255, 0.5)" sx={{ fontSize: '0.8rem', fontFamily: 'inherit' }}>
            -
          </Typography>
        </Box>
      );
    }

    return (
      <Box
        sx={{
          backgroundColor: 'rgba(255, 255, 255, 0.1)',
          border: '1px solid rgba(255, 255, 255, 0.2)',
          borderRadius: 1,
          padding: '4px 6px',
          textAlign: 'center',
          minHeight: 40,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          width: '100%',
          boxSizing: 'border-box',
        }}
      >
        <Typography variant="body2" fontWeight="bold" sx={{ 
          fontSize: '0.8rem',
          lineHeight: 1.2,
          wordBreak: 'break-word',
          color: '#ffffff',
          fontFamily: 'inherit'
        }}>
          {slotContent}
        </Typography>
      </Box>
    );
  };

  return (
    <Box
      sx={{ 
        width: '100vw',
        height: '100vh',
        overflow: 'auto',
        padding: 1,
        borderRadius: '0px',
        // Mac-style glassmorphism - single container that fills screen
        backgroundColor: 'rgba(255, 255, 255, 0.08)',
        backdropFilter: 'blur(20px)',
        border: 'none',
        boxShadow: 'none',
        fontFamily: "'Elms Sans', 'Inter', 'Segoe UI', Roboto, sans-serif",
      }}
    >
        <Table 
          size="small" 
          sx={{ 
            tableLayout: 'fixed',
            width: '100%',
            borderCollapse: 'collapse',
            borderRadius: '20px',
            overflow: 'hidden',
            backgroundColor: 'transparent',
            // Rose red shadow on table border
            boxShadow: '0 0 20px rgba(225, 29, 72, 0.4), inset 0 0 20px rgba(225, 29, 72, 0.1)',
            '& .MuiTableCell-root': {
              border: '1px solid rgba(255, 255, 255, 0.1)',
              verticalAlign: 'middle',
              padding: 0,
              backgroundColor: 'transparent',
              color: '#ffffff',
            },
            '& .MuiTableRow-root:hover': {
              backgroundColor: 'rgba(255, 255, 255, 0.05)',
            },
          }}
        >
          {/* Theory Hours Row */}
          <TableHead>
            <TableRow>
              <TableCell 
                sx={{ 
                  backgroundColor: 'rgba(255, 255, 255, 0.15)',
                  color: 'white',
                  fontWeight: 'bold',
                  width: '70px',
                  padding: '4px',
                  textAlign: 'center',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                }}
              >
                <Typography variant="caption" fontWeight="bold" sx={{ fontSize: '0.7rem', fontFamily: 'inherit' }}>
                  THEORY HOURS
                </Typography>
              </TableCell>
              {THEORY_HOURS.map((time, index) => (
                <TableCell 
                  key={index}
                  sx={{ 
                    backgroundColor: 'transparent',
                    fontWeight: 'bold',
                    width: `${100/14}%`,
                    padding: '6px 2px',
                    textAlign: 'center',
                    verticalAlign: 'middle',
                    height: '70px',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                  }}
                >
                  {renderTimeCell(time)}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>

          {/* Lab Hours Row */}
          <TableBody>
            <TableRow>
              <TableCell 
                sx={{ 
                  backgroundColor: 'rgba(255, 255, 255, 0.12)',
                  color: 'white',
                  fontWeight: 'bold',
                  padding: '4px',
                  textAlign: 'center',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                }}
              >
                <Typography variant="caption" fontWeight="bold" sx={{ fontSize: '0.7rem', fontFamily: 'inherit' }}>
                  LAB HOURS
                </Typography>
              </TableCell>
              {LAB_HOURS.map((time, index) => (
                <TableCell 
                  key={index}
                  sx={{ 
                    backgroundColor: 'transparent',
                    fontWeight: 'bold',
                    padding: '6px 2px',
                    textAlign: 'center',
                    verticalAlign: 'middle',
                    height: '70px',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                  }}
                >
                  {renderTimeCell(time)}
                </TableCell>
              ))}
            </TableRow>

            {/* Days and Timetable Data */}
            {DAYS.map((day, dayIndex) => (
              <TableRow 
                key={day}
                sx={{ 
                  height: 60,
                }}
              >
                <TableCell 
                  sx={{ 
                    backgroundColor: 'rgba(255, 255, 255, 0.15)',
                    color: 'white',
                    fontWeight: 'bold',
                    padding: '4px',
                    textAlign: 'center',
                    verticalAlign: 'middle',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                  }}
                >
                  <Typography variant="body2" fontWeight="bold" sx={{ fontFamily: 'inherit' }}>
                    {day}
                  </Typography>
                </TableCell>
                {DAY_SLOT_MAPPING[day].map((slotContent, timeIndex) => (
                  <TableCell
                    key={`${day}-${timeIndex}`}
                    sx={{
                      padding: '2px',
                      textAlign: 'center',
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
    </Box>
  );
};

export default TimetableGrid;