// Course data service for handling CSV data
export interface Course {
  courseCode: string;
  courseName: string;
  slot: string;
  venue: string;
  faculty: string;
  type: string;
  curriculum: string;
  credits?: number;
}

export interface CourseInfo {
  courseCode: string;
  courseTitle: string;
  courseType: string;
  credits: number;
  L: number;
  T: number;
  P: number;
  J: number;
}

// Mock data based on CSV structure - in a real app, this would load from the server
export const mockCourses: Course[] = [
  {
    courseCode: "BCHY101L",
    courseName: "Engineering Chemistry",
    slot: "C2",
    venue: "PRP735",
    faculty: "SATHISH KUMAR P",
    type: "TH",
    curriculum: "FC - Foundation Core",
    credits: 3
  },
  {
    courseCode: "BCSE101E",
    courseName: "Computer Programming: Python",
    slot: "A1",
    venue: "SCOPE Lab1",
    faculty: "Dr. RAJESH KUMAR",
    type: "LAB",
    curriculum: "PC - Program Core",
    credits: 3
  },
  {
    courseCode: "BMAT101L",
    courseName: "Calculus for Engineers",
    slot: "F1",
    venue: "SJT201",
    faculty: "Dr. PRIYA SHARMA",
    type: "TH",
    curriculum: "FC - Foundation Core",
    credits: 4
  },
  {
    courseCode: "BENG101L",
    courseName: "Technical English Communication",
    slot: "D1",
    venue: "SJT115",
    faculty: "Prof. MARY JOSEPH",
    type: "TH",
    curriculum: "FC - Foundation Core",
    credits: 2
  },
  {
    courseCode: "BEEE102L",
    courseName: "Basic Electrical and Electronics Engineering",
    slot: "B1",
    venue: "ECE Lab",
    faculty: "Dr. SURESH BABU",
    type: "LAB",
    curriculum: "PC - Program Core",
    credits: 3
  },
  {
    courseCode: "JAVA101L",
    courseName: "Java Programming Fundamentals",
    slot: "G1",
    venue: "SCOPE Lab2",
    faculty: "Dr. JAMES WILSON",
    type: "LAB",
    curriculum: "PC - Program Core",
    credits: 3
  },
  {
    courseCode: "JAVASCRIPT101L",
    courseName: "JavaScript for Web Development",
    slot: "E1",
    venue: "IT Lab1",
    faculty: "Prof. JOHN ADAMS",
    type: "LAB",
    curriculum: "PE - Program Elective",
    credits: 2
  },
  {
    courseCode: "JDATABASE101L",
    courseName: "Database Management Systems",
    slot: "A2",
    venue: "SJT301",
    faculty: "Dr. JANET COOPER",
    type: "TH",
    curriculum: "PC - Program Core",
    credits: 4
  },
  {
    courseCode: "PHYSICS101L",
    courseName: "Physics for Engineers",
    slot: "B2",
    venue: "Physics Lab",
    faculty: "Dr. PETER JONES",
    type: "TH",
    curriculum: "FC - Foundation Core",
    credits: 3
  },
  {
    courseCode: "PYTHON101L",
    courseName: "Python Programming Advanced",
    slot: "C1",
    venue: "SCOPE Lab3",
    faculty: "Prof. PATRICIA BROWN",
    type: "LAB",
    curriculum: "PE - Program Elective",
    credits: 3
  },
  {
    courseCode: "ALGORITHMS101L",
    courseName: "Algorithms and Data Structures",
    slot: "F2",
    venue: "SJT401",
    faculty: "Dr. ALEX TURNER",
    type: "TH",
    curriculum: "PC - Program Core",
    credits: 4
  },
  {
    courseCode: "NETWORKS101L",
    courseName: "Computer Networks",
    slot: "D2",
    venue: "Network Lab",
    faculty: "Prof. NANCY DAVIS",
    type: "LAB",
    curriculum: "PC - Program Core",
    credits: 3
  }
];

export const searchCourses = (query: string): Course[] => {
  if (!query || query.trim() === '') return [];
  
  const lowercaseQuery = query.toLowerCase().trim();
  return mockCourses.filter(course => 
    course.courseName.toLowerCase().includes(lowercaseQuery) ||
    course.courseCode.toLowerCase().includes(lowercaseQuery) ||
    course.faculty.toLowerCase().includes(lowercaseQuery) ||
    course.courseName.toLowerCase().startsWith(lowercaseQuery) ||
    course.courseCode.toLowerCase().startsWith(lowercaseQuery)
  );
};

export const getCourseByCode = (courseCode: string): Course | undefined => {
  return mockCourses.find(course => course.courseCode === courseCode);
};

export const getCoursesByFaculty = (faculty: string): Course[] => {
  return mockCourses.filter(course => 
    course.faculty.toLowerCase().includes(faculty.toLowerCase())
  );
};