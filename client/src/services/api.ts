import axios from 'axios';
import {
  Course,
  Teacher,
  FacultyGroup,
  TimetableSummary,
  ApiResponse,
  AutocompleteOption,
  Conflict
} from '../types';

// API base configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Response Error:', error);
    if (error.response?.status === 404) {
      console.warn('API endpoint not found:', error.config.url);
    }
    return Promise.reject(error);
  }
);

// Course API methods
export const courseApi = {
  // Get all courses with optional search
  getCourses: async (search?: string, type?: string, limit?: number): Promise<Course[]> => {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (type) params.append('type', type);
    if (limit) params.append('limit', limit.toString());

    const response = await api.get<ApiResponse<Course[]>>(`/courses?${params}`);
    return response.data.data || [];
  },

  // Get specific course by code
  getCourse: async (courseCode: string): Promise<Course | null> => {
    try {
      const response = await api.get<ApiResponse<Course>>(`/courses/${courseCode}`);
      return response.data.data || null;
    } catch (error) {
      return null;
    }
  },

  // Get courses for autocomplete
  getCoursesAutocomplete: async (query: string): Promise<AutocompleteOption[]> => {
    if (query.length < 2) return [];
    
    const response = await api.get<ApiResponse<AutocompleteOption[]>>(
      `/courses/search/autocomplete?q=${encodeURIComponent(query)}&limit=10`
    );
    return response.data.data || [];
  },

  // Get course statistics
  getCourseStats: async () => {
    const response = await api.get<ApiResponse<any>>('/courses/admin/stats');
    return response.data.data;
  },

  // Reload course data
  reloadCourseData: async () => {
    const response = await api.post<ApiResponse<any>>('/courses/admin/reload');
    return response.data;
  }
};

// Teacher API methods
export const teacherApi = {
  // Get all teachers with optional filters
  getTeachers: async (filters?: {
    search?: string;
    courseCode?: string;
    faculty?: string;
    type?: string;
    limit?: number;
  }): Promise<Teacher[]> => {
    const params = new URLSearchParams();
    if (filters?.search) params.append('search', filters.search);
    if (filters?.courseCode) params.append('courseCode', filters.courseCode);
    if (filters?.faculty) params.append('faculty', filters.faculty);
    if (filters?.type) params.append('type', filters.type);
    if (filters?.limit) params.append('limit', filters.limit.toString());

    const response = await api.get<ApiResponse<Teacher[]>>(`/teachers?${params}`);
    return response.data.data || [];
  },

  // Get teachers for a specific course
  getTeachersByCourse: async (courseCode: string, type?: string): Promise<FacultyGroup[]> => {
    const params = new URLSearchParams();
    if (type) params.append('type', type);

    const response = await api.get<ApiResponse<FacultyGroup[]>>(
      `/teachers/course/${courseCode}?${params}`
    );
    return response.data.data || [];
  },

  // Get courses taught by a faculty
  getCoursesByFaculty: async (facultyName: string) => {
    const response = await api.get<ApiResponse<any>>(`/teachers/faculty/${facultyName}`);
    return response.data;
  },

  // Get teachers for autocomplete
  getFacultyAutocomplete: async (query: string): Promise<AutocompleteOption[]> => {
    if (query.length < 2) return [];
    
    const response = await api.get<ApiResponse<AutocompleteOption[]>>(
      `/teachers/search/autocomplete?q=${encodeURIComponent(query)}&limit=10`
    );
    return response.data.data || [];
  },

  // Get teachers in a specific slot
  getTeachersBySlot: async (slot: string): Promise<Teacher[]> => {
    const response = await api.get<ApiResponse<Teacher[]>>(`/teachers/slots/${slot}`);
    return response.data.data || [];
  }
};

// Timetable API methods
export const timetableApi = {
  // Get current timetable
  getTimetable: async (userId?: string): Promise<TimetableSummary> => {
    const params = userId ? `?userId=${userId}` : '';
    const response = await api.get<ApiResponse<{ summary: TimetableSummary }>>(
      `/timetable${params}`
    );
    return response.data.data?.summary || {
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
    };
  },

  // Add course to timetable
  addCourse: async (
    courseCode: string,
    facultyName: string,
    slot: string,
    venue?: string,
    userId?: string
  ): Promise<{ success: boolean; courseId?: number; conflicts?: Conflict[] }> => {
    const response = await api.post<ApiResponse<{ courseId: number; timetable: TimetableSummary }>>(
      '/timetable/add-course',
      {
        courseCode,
        facultyName,
        slot,
        venue,
        userId
      }
    );

    if (response.data.success) {
      return {
        success: true,
        courseId: response.data.data?.courseId
      };
    } else {
      return {
        success: false,
        conflicts: (response.data as any).conflicts
      };
    }
  },

  // Remove course from timetable
  removeCourse: async (courseId: number, userId?: string): Promise<boolean> => {
    const params = userId ? `?userId=${userId}` : '';
    const response = await api.delete<ApiResponse<any>>(
      `/timetable/remove-course/${courseId}${params}`
    );
    return response.data.success;
  },

  // Clear entire timetable
  clearTimetable: async (userId?: string): Promise<boolean> => {
    const response = await api.post<ApiResponse<any>>('/timetable/clear', { userId });
    return response.data.success;
  },

  // Check for conflicts
  checkConflicts: async (
    courseCode: string,
    facultyName: string,
    slot: string,
    userId?: string
  ): Promise<Conflict[]> => {
    const response = await api.post<ApiResponse<{
      hasConflicts: boolean;
      conflicts: Conflict[];
    }>>('/timetable/check-conflicts', {
      courseCode,
      facultyName,
      slot,
      userId
    });

    return response.data.data?.conflicts || [];
  },

  // Get timetable summary
  getTimetableSummary: async (userId?: string) => {
    const params = userId ? `?userId=${userId}` : '';
    const response = await api.get<ApiResponse<TimetableSummary>>(`/timetable/summary${params}`);
    return response.data.data;
  },

  // Export timetable
  exportTimetable: async (format: 'json' | 'csv' = 'json', userId?: string) => {
    const params = new URLSearchParams();
    params.append('format', format);
    if (userId) params.append('userId', userId);

    const response = await api.get(`/timetable/export?${params}`, {
      responseType: format === 'csv' ? 'blob' : 'json'
    });

    return response.data;
  }
};

// Health check
export const healthApi = {
  checkHealth: async () => {
    const response = await api.get<ApiResponse<any>>('/health');
    return response.data;
  }
};

export default api;