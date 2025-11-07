// Course interface
export interface Course {
  serialNumber: number;
  courseCode: string;
  courseTitle: string;
  courseType: string;
  version: string;
  lectureHours: number;
  tutorialHours: number;
  practicalHours: number;
  projectHours: number;
  credits: number;
  totalHours: number;
}

// Teacher interface
export interface Teacher {
  curriculum: string;
  courseCode: string;
  courseName: string;
  slot: string;
  slots: string[];
  venue: string;
  faculty: string;
  type: string;
  timings: SlotTiming[];
}

// Slot timing interface
export interface SlotTiming {
  slot: string;
  timing: {
    day: string;
    time: string;
  };
}

// Timetable entry interface
export interface TimetableEntry {
  courseCode: string;
  courseTitle: string;
  faculty: string;
  venue: string;
  type: string;
  time: string;
  credits: number;
}

// Timetable schedule interface
export interface TimetableSchedule {
  Monday: { [slot: string]: TimetableEntry[] };
  Tuesday: { [slot: string]: TimetableEntry[] };
  Wednesday: { [slot: string]: TimetableEntry[] };
  Thursday: { [slot: string]: TimetableEntry[] };
  Friday: { [slot: string]: TimetableEntry[] };
}

// Course entry in timetable
export interface CourseEntry {
  id: number;
  course: Course;
  teacher: Teacher;
  slots: SlotTiming[];
  addedAt: string;
}

// Timetable summary
export interface TimetableSummary {
  totalCourses: number;
  totalCredits: number;
  schedule: TimetableSchedule;
  courses: {
    courseCode: string;
    courseTitle: string;
    faculty: string;
    credits: number;
    slots: string;
  }[];
  conflicts: Conflict[];
}

// Conflict interface
export interface Conflict {
  slot: string;
  day: string;
  time: string;
  existingCourse: string;
  message: string;
}

// API Response interfaces
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
  count?: number;
}

// Search/Autocomplete interfaces
export interface AutocompleteOption {
  label: string;
  value: string;
  courseCode?: string;
  courseTitle?: string;
  courseType?: string;
  credits?: number;
}

// Faculty group interface for teacher selection
export interface FacultyGroup {
  faculty: string;
  slots: {
    slot: string;
    venue: string;
    type: string;
    timings: SlotTiming[];
  }[];
  types: string[];
}

// Timetable context interface
export interface TimetableContextType {
  timetable: TimetableSummary | null;
  loading: boolean;
  error: string | null;
  addCourse: (courseCode: string, facultyName: string, slot: string, venue?: string) => Promise<boolean>;
  removeCourse: (courseId: number) => Promise<boolean>;
  clearTimetable: () => Promise<boolean>;
  refreshTimetable: () => Promise<void>;
  checkConflicts: (courseCode: string, facultyName: string, slot: string) => Promise<Conflict[]>;
}