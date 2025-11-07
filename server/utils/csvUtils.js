const fs = require('fs');
const path = require('path');
const { parse } = require('csv-parse');
const Course = require('../models/Course');
const Teacher = require('../models/Teacher');

class CSVUtils {
  constructor() {
    this.coursesCache = null;
    this.teachersCache = null;
    this.dataPath = path.join(__dirname, '../../data');
  }

  // Read and parse CSV file
  async readCSV(filePath) {
    return new Promise((resolve, reject) => {
      const results = [];
      const stream = fs.createReadStream(filePath)
        .pipe(parse({ 
          columns: true, 
          skip_empty_lines: true,
          trim: true 
        }));

      stream.on('data', (data) => {
        results.push(data);
      });

      stream.on('error', (error) => {
        console.error(`Error reading CSV file ${filePath}:`, error);
        reject(error);
      });

      stream.on('end', () => {
        console.log(`✅ Successfully loaded ${results.length} records from ${path.basename(filePath)}`);
        resolve(results);
      });
    });
  }

  // Load courses from CSV
  async loadCourses(forceReload = false) {
    if (this.coursesCache && !forceReload) {
      return this.coursesCache;
    }

    try {
      const coursesPath = path.join(this.dataPath, 'courses.csv');
      const rawData = await this.readCSV(coursesPath);
      
      this.coursesCache = rawData.map(row => new Course(row));
      console.log(`📚 Loaded ${this.coursesCache.length} courses`);
      
      return this.coursesCache;
    } catch (error) {
      console.error('Error loading courses:', error);
      throw new Error('Failed to load courses data');
    }
  }

  // Load teachers from CSV
  async loadTeachers(forceReload = false) {
    if (this.teachersCache && !forceReload) {
      return this.teachersCache;
    }

    try {
      const teachersPath = path.join(this.dataPath, 'all_teachers.csv');
      const rawData = await this.readCSV(teachersPath);
      
      this.teachersCache = rawData.map(row => new Teacher(row));
      console.log(`👨‍🏫 Loaded ${this.teachersCache.length} teacher records`);
      
      return this.teachersCache;
    } catch (error) {
      console.error('Error loading teachers:', error);
      throw new Error('Failed to load teachers data');
    }
  }

  // Search courses by code or title
  async searchCourses(query) {
    const courses = await this.loadCourses();
    
    if (!query) return courses;
    
    const searchTerm = query.toLowerCase();
    return courses.filter(course => 
      course.courseCode.toLowerCase().includes(searchTerm) ||
      course.courseTitle.toLowerCase().includes(searchTerm)
    );
  }

  // Get course by code
  async getCourseByCode(courseCode) {
    const courses = await this.loadCourses();
    return courses.find(course => 
      course.courseCode.toLowerCase() === courseCode.toLowerCase()
    );
  }

  // Search teachers by course code
  async getTeachersByCourse(courseCode) {
    const teachers = await this.loadTeachers();
    return teachers.filter(teacher => 
      teacher.courseCode.toLowerCase() === courseCode.toLowerCase()
    );
  }

  // Search teachers by faculty name
  async searchTeachers(query) {
    const teachers = await this.loadTeachers();
    
    if (!query) return teachers;
    
    const searchTerm = query.toLowerCase();
    return teachers.filter(teacher => 
      teacher.faculty.toLowerCase().includes(searchTerm) ||
      teacher.courseCode.toLowerCase().includes(searchTerm) ||
      teacher.courseName.toLowerCase().includes(searchTerm)
    );
  }

  // Get all unique course codes from teachers data
  async getAvailableCourses() {
    const teachers = await this.loadTeachers();
    const courses = await this.loadCourses();
    
    const courseMap = new Map();
    
    // Add courses from main courses.csv
    courses.forEach(course => {
      courseMap.set(course.courseCode, {
        ...course.toJSON(),
        hasTeachers: false
      });
    });
    
    // Mark courses that have teachers available
    teachers.forEach(teacher => {
      if (courseMap.has(teacher.courseCode)) {
        courseMap.get(teacher.courseCode).hasTeachers = true;
      } else {
        // Add courses that exist in teachers data but not in courses.csv
        courseMap.set(teacher.courseCode, {
          courseCode: teacher.courseCode,
          courseTitle: teacher.courseName,
          courseType: teacher.type === 'TH' ? 'Theory Only' : 'Lab Only',
          hasTeachers: true
        });
      }
    });
    
    return Array.from(courseMap.values());
  }

  // Get statistics about the data
  async getDataStats() {
    const courses = await this.loadCourses();
    const teachers = await this.loadTeachers();
    
    const courseTypes = {};
    courses.forEach(course => {
      courseTypes[course.courseType] = (courseTypes[course.courseType] || 0) + 1;
    });
    
    const faculties = new Set(teachers.map(t => t.faculty)).size;
    const uniqueCourses = new Set(teachers.map(t => t.courseCode)).size;
    
    return {
      totalCourses: courses.length,
      totalTeacherRecords: teachers.length,
      uniqueFaculties: faculties,
      uniqueCoursesWithTeachers: uniqueCourses,
      courseTypes: courseTypes,
      lastUpdated: new Date().toISOString()
    };
  }

  // Reload all data
  async reloadData() {
    console.log('🔄 Reloading all CSV data...');
    this.coursesCache = null;
    this.teachersCache = null;
    
    await Promise.all([
      this.loadCourses(true),
      this.loadTeachers(true)
    ]);
    
    console.log('✅ Data reload completed');
    return await this.getDataStats();
  }
}

// Create singleton instance
const csvUtils = new CSVUtils();

module.exports = csvUtils;