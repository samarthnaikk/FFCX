import React from 'react';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  Container,
  AppBar,
  Toolbar,
  Typography,
  Box,
  Paper,
} from '@mui/material';
import {
  Schedule as ScheduleIcon,
} from '@mui/icons-material';
import TimetableGrid from './components/TimetableGrid';
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

// Main App Component
function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1 }}>
        {/* App Bar */}
        <AppBar position="static" elevation={2}>
          <Toolbar>
            <ScheduleIcon sx={{ mr: 2 }} />
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              FFCX - Timetable Optimizer
            </Typography>
          </Toolbar>
        </AppBar>

        <Container maxWidth="xl" sx={{ mt: 3, mb: 3 }}>
          {/* Timetable Grid Section */}
          <Paper elevation={2} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Weekly Timetable
            </Typography>
            <TimetableGrid />
          </Paper>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;