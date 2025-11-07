const express = require('express');
const csvUtils = require('../utils/csvUtils');
const router = express.Router();

// @route   GET /api/teachers
// @desc    Get all teachers or search teachers
// @access  Public
router.get('/', async (req, res) => {
  try {
    const { search, courseCode, faculty, type, limit = 50 } = req.query;
    
    let teachers;
    
    if (courseCode) {
      teachers = await csvUtils.getTeachersByCourse(courseCode);
    } else if (search) {
      teachers = await csvUtils.searchTeachers(search);
    } else {
      teachers = await csvUtils.loadTeachers();
    }

    // Additional filters
    if (faculty) {
      teachers = teachers.filter(teacher => 
        teacher.faculty.toLowerCase().includes(faculty.toLowerCase())
      );
    }

    if (type) {
      teachers = teachers.filter(teacher => 
        teacher.type.toLowerCase() === type.toLowerCase()
      );
    }

    // Apply limit
    const limitNum = parseInt(limit);
    if (limitNum > 0 && teachers.length > limitNum) {
      teachers = teachers.slice(0, limitNum);
    }

    res.json({
      success: true,
      count: teachers.length,
      data: teachers.map(teacher => teacher.toJSON())
    });
  } catch (error) {
    console.error('Error fetching teachers:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch teachers',
      message: error.message
    });
  }
});

// @route   GET /api/teachers/course/:courseCode
// @desc    Get all teachers for a specific course
// @access  Public
router.get('/course/:courseCode', async (req, res) => {
  try {
    const { courseCode } = req.params;
    const { type } = req.query; // 'TH' for theory, 'LAB' for lab
    
    let teachers = await csvUtils.getTeachersByCourse(courseCode);
    
    if (type) {
      teachers = teachers.filter(teacher => teacher.type === type.toUpperCase());
    }

    // Group teachers by faculty for easier selection
    const groupedTeachers = teachers.reduce((acc, teacher) => {
      const faculty = teacher.faculty;
      if (!acc[faculty]) {
        acc[faculty] = {
          faculty: faculty,
          slots: [],
          types: new Set()
        };
      }
      
      acc[faculty].slots.push({
        slot: teacher.slot,
        venue: teacher.venue,
        type: teacher.type,
        timings: teacher.getSlotTimings()
      });
      acc[faculty].types.add(teacher.type);
      
      return acc;
    }, {});

    // Convert to array and clean up
    const result = Object.values(groupedTeachers).map(group => ({
      ...group,
      types: Array.from(group.types)
    }));

    res.json({
      success: true,
      courseCode: courseCode,
      count: result.length,
      totalSlots: teachers.length,
      data: result
    });
  } catch (error) {
    console.error('Error fetching teachers for course:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch teachers for course',
      message: error.message
    });
  }
});

// @route   GET /api/teachers/faculty/:facultyName
// @desc    Get all courses taught by a specific faculty
// @access  Public
router.get('/faculty/:facultyName', async (req, res) => {
  try {
    const { facultyName } = req.params;
    const teachers = await csvUtils.loadTeachers();
    
    const facultyTeachers = teachers.filter(teacher => 
      teacher.faculty.toLowerCase().includes(facultyName.toLowerCase())
    );

    if (facultyTeachers.length === 0) {
      return res.status(404).json({
        success: false,
        error: 'Faculty not found',
        message: `No faculty found matching: ${facultyName}`
      });
    }

    // Group by course
    const coursesByFaculty = facultyTeachers.reduce((acc, teacher) => {
      const courseCode = teacher.courseCode;
      if (!acc[courseCode]) {
        acc[courseCode] = {
          courseCode: courseCode,
          courseName: teacher.courseName,
          curriculum: teacher.curriculum,
          slots: []
        };
      }
      
      acc[courseCode].slots.push({
        slot: teacher.slot,
        venue: teacher.venue,
        type: teacher.type,
        timings: teacher.getSlotTimings()
      });
      
      return acc;
    }, {});

    res.json({
      success: true,
      faculty: facultyName,
      count: Object.keys(coursesByFaculty).length,
      totalSlots: facultyTeachers.length,
      data: Object.values(coursesByFaculty)
    });
  } catch (error) {
    console.error('Error fetching faculty courses:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch faculty courses',
      message: error.message
    });
  }
});

// @route   GET /api/teachers/slots/:slot
// @desc    Get all teachers teaching in a specific slot
// @access  Public
router.get('/slots/:slot', async (req, res) => {
  try {
    const { slot } = req.params;
    const teachers = await csvUtils.loadTeachers();
    
    const slotTeachers = teachers.filter(teacher => {
      const teacherSlots = teacher.getSlots();
      return teacherSlots.includes(slot.toUpperCase());
    });

    res.json({
      success: true,
      slot: slot.toUpperCase(),
      count: slotTeachers.length,
      data: slotTeachers.map(teacher => teacher.toJSON())
    });
  } catch (error) {
    console.error('Error fetching slot teachers:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch slot teachers',
      message: error.message
    });
  }
});

// @route   GET /api/teachers/search/autocomplete
// @desc    Get faculty names for autocomplete
// @access  Public
router.get('/search/autocomplete', async (req, res) => {
  try {
    const { q, limit = 10 } = req.query;
    
    if (!q || q.length < 2) {
      return res.json({
        success: true,
        count: 0,
        data: []
      });
    }

    const teachers = await csvUtils.loadTeachers();
    
    // Get unique faculty names that match the search
    const facultySet = new Set();
    teachers.forEach(teacher => {
      if (teacher.faculty.toLowerCase().includes(q.toLowerCase())) {
        facultySet.add(teacher.faculty);
      }
    });

    const facultyArray = Array.from(facultySet)
      .slice(0, parseInt(limit))
      .map(faculty => ({
        label: faculty,
        value: faculty
      }));

    res.json({
      success: true,
      count: facultyArray.length,
      data: facultyArray
    });
  } catch (error) {
    console.error('Error in faculty autocomplete:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to perform faculty autocomplete',
      message: error.message
    });
  }
});

module.exports = router;