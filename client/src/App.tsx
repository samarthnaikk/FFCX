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
      <Box sx={{ 
        width: '100vw', 
        height: '100vh', 
        backgroundColor: '#000000',
        overflow: 'hidden'
      }}>
        <TimetableGrid />
      </Box>
    </ThemeProvider>
  );
}

export default App;