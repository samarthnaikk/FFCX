import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { TimetableContextType, TimetableSummary, Conflict } from '../types';
import { timetableApi } from '../services/api';

// Action types
type TimetableAction =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_TIMETABLE'; payload: TimetableSummary }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'CLEAR_TIMETABLE' };

// Initial state
interface TimetableState {
  timetable: TimetableSummary | null;
  loading: boolean;
  error: string | null;
}

const initialState: TimetableState = {
  timetable: null,
  loading: false,
  error: null,
};

// Reducer
const timetableReducer = (state: TimetableState, action: TimetableAction): TimetableState => {
  switch (action.type) {
    case 'SET_LOADING':
      return {
        ...state,
        loading: action.payload,
        error: action.payload ? null : state.error, // Clear error when loading starts
      };
    case 'SET_TIMETABLE':
      return {
        ...state,
        timetable: action.payload,
        loading: false,
        error: null,
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
        loading: false,
      };
    case 'CLEAR_TIMETABLE':
      return {
        ...state,
        timetable: {
          totalCourses: 0,
          totalCredits: 0,
          schedule: {
            Monday: {},
            Tuesday: {},
            Wednesday: {},
            Thursday: {},
            Friday: {}
          },
          courses: [],
          conflicts: []
        },
        error: null,
      };
    default:
      return state;
  }
};

// Context
const TimetableContext = createContext<TimetableContextType | undefined>(undefined);

// Provider component
export const TimetableProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(timetableReducer, initialState);

  // Load timetable on mount
  useEffect(() => {
    refreshTimetable();
  }, []);

  const refreshTimetable = async (): Promise<void> => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const timetableData = await timetableApi.getTimetable();
      dispatch({ type: 'SET_TIMETABLE', payload: timetableData });
    } catch (error) {
      console.error('Failed to load timetable:', error);
      dispatch({ type: 'SET_ERROR', payload: 'Failed to load timetable' });
    }
  };

  const addCourse = async (
    courseCode: string,
    facultyName: string,
    slot: string,
    venue?: string
  ): Promise<boolean> => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const result = await timetableApi.addCourse(courseCode, facultyName, slot, venue);
      
      if (result.success) {
        // Refresh timetable after successful addition
        await refreshTimetable();
        return true;
      } else {
        const conflictMessages = result.conflicts?.map(c => c.message).join(', ') || 'Unknown conflict';
        dispatch({ type: 'SET_ERROR', payload: `Cannot add course: ${conflictMessages}` });
        return false;
      }
    } catch (error: any) {
      console.error('Failed to add course:', error);
      let errorMessage = 'Failed to add course';
      
      if (error.response?.status === 409) {
        errorMessage = 'Slot conflict detected';
      } else if (error.response?.status === 404) {
        errorMessage = 'Course or teacher not found';
      } else if (error.response?.data?.message) {
        errorMessage = error.response.data.message;
      }
      
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      return false;
    }
  };

  const removeCourse = async (courseId: number): Promise<boolean> => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const success = await timetableApi.removeCourse(courseId);
      
      if (success) {
        // Refresh timetable after successful removal
        await refreshTimetable();
        return true;
      } else {
        dispatch({ type: 'SET_ERROR', payload: 'Failed to remove course' });
        return false;
      }
    } catch (error: any) {
      console.error('Failed to remove course:', error);
      dispatch({ type: 'SET_ERROR', payload: 'Failed to remove course' });
      return false;
    }
  };

  const clearTimetable = async (): Promise<boolean> => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const success = await timetableApi.clearTimetable();
      
      if (success) {
        dispatch({ type: 'CLEAR_TIMETABLE' });
        return true;
      } else {
        dispatch({ type: 'SET_ERROR', payload: 'Failed to clear timetable' });
        return false;
      }
    } catch (error: any) {
      console.error('Failed to clear timetable:', error);
      dispatch({ type: 'SET_ERROR', payload: 'Failed to clear timetable' });
      return false;
    }
  };

  const checkConflicts = async (
    courseCode: string,
    facultyName: string,
    slot: string
  ): Promise<Conflict[]> => {
    try {
      return await timetableApi.checkConflicts(courseCode, facultyName, slot);
    } catch (error) {
      console.error('Failed to check conflicts:', error);
      return [];
    }
  };

  const contextValue: TimetableContextType = {
    timetable: state.timetable,
    loading: state.loading,
    error: state.error,
    addCourse,
    removeCourse,
    clearTimetable,
    refreshTimetable,
    checkConflicts,
  };

  return (
    <TimetableContext.Provider value={contextValue}>
      {children}
    </TimetableContext.Provider>
  );
};

// Custom hook to use timetable context
export const useTimetable = (): TimetableContextType => {
  const context = useContext(TimetableContext);
  if (context === undefined) {
    throw new Error('useTimetable must be used within a TimetableProvider');
  }
  return context;
};

export default TimetableContext;