const express = require('express');
const csvUtils = require('../utils/csvUtils');
const Timetable = require('../models/Timetable');
const Course = require('../models/Course');
const Teacher = require('../models/Teacher');
const router = express.Router();

// In-memory storage for user timetables (should be replaced with database)
const userTimetables = new Map();

// Helper function to get or create timetable for user
function getUserTimetable(userId = 'default') {
  if (!userTimetables.has(userId)) {
    userTimetables.set(userId, new Timetable());
  }
  return userTimetables.get(userId);
}

// @route   GET /api/timetable
// @desc    Get current timetable
// @access  Public
router.get('/', (req, res) => {
  try {
    const { userId = 'default' } = req.query;
    const timetable = getUserTimetable(userId);
    
    res.json({
      success: true,
      data: timetable.toJSON()
    });
  } catch (error) {
    console.error('Error fetching timetable:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch timetable',
      message: error.message
    });
  }
});

// @route   POST /api/timetable/add-course
// @desc    Add a course to the timetable
// @access  Public
router.post('/add-course', async (req, res) => {
  try {
    const { 
      courseCode, 
      facultyName, 
      slot, 
      venue,
      userId = 'default' 
    } = req.body;

    // Validate required fields
    if (!courseCode || !facultyName || !slot) {
      return res.status(400).json({
        success: false,
        error: 'Missing required fields',
        message: 'courseCode, facultyName, and slot are required'
      });
    }

    // Get course details
    const course = await csvUtils.getCourseByCode(courseCode);
    if (!course) {
      return res.status(404).json({
        success: false,
        error: 'Course not found',
        message: `No course found with code: ${courseCode}`
      });
    }

    // Find matching teacher
    const teachers = await csvUtils.getTeachersByCourse(courseCode);
    const teacher = teachers.find(t => 
      t.faculty === facultyName && t.slot === slot
    );

    if (!teacher) {
      return res.status(404).json({
        success: false,
        error: 'Teacher not found',
        message: `No teacher found for course ${courseCode} with faculty ${facultyName} in slot ${slot}`
      });
    }

    // Get timetable and add course
    const timetable = getUserTimetable(userId);
    const slotTimings = teacher.getSlotTimings();
    const result = timetable.addCourse(course, teacher, slotTimings);

    if (!result.success) {
      return res.status(409).json({
        success: false,
        error: 'Slot conflict detected',
        conflicts: result.conflicts
      });
    }

    res.json({
      success: true,
      message: 'Course added successfully',
      data: {
        courseId: result.courseId,
        timetable: timetable.getSummary()
      }
    });
  } catch (error) {
    console.error('Error adding course:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to add course',
      message: error.message
    });
  }
});

// @route   DELETE /api/timetable/remove-course/:courseId
// @desc    Remove a course from the timetable
// @access  Public
router.delete('/remove-course/:courseId', (req, res) => {
  try {
    const { courseId } = req.params;
    const { userId = 'default' } = req.query;

    const timetable = getUserTimetable(userId);
    const result = timetable.removeCourse(parseInt(courseId));

    if (!result.success) {
      return res.status(404).json({
        success: false,
        error: 'Course not found',
        message: result.message
      });
    }

    res.json({
      success: true,
      message: 'Course removed successfully',
      data: {
        timetable: timetable.getSummary()
      }
    });
  } catch (error) {
    console.error('Error removing course:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to remove course',
      message: error.message
    });
  }
});

// @route   POST /api/timetable/clear
// @desc    Clear entire timetable
// @access  Public
router.post('/clear', (req, res) => {
  try {
    const { userId = 'default' } = req.body;
    const timetable = getUserTimetable(userId);
    timetable.clear();

    res.json({
      success: true,
      message: 'Timetable cleared successfully',
      data: {
        timetable: timetable.getSummary()
      }
    });
  } catch (error) {
    console.error('Error clearing timetable:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to clear timetable',
      message: error.message
    });
  }
});

// @route   GET /api/timetable/summary
// @desc    Get timetable summary with statistics
// @access  Public
router.get('/summary', (req, res) => {
  try {
    const { userId = 'default' } = req.query;
    const timetable = getUserTimetable(userId);
    const summary = timetable.getSummary();

    // Add additional statistics
    const stats = {
      ...summary,
      averageCreditsPerCourse: summary.totalCourses > 0 ? 
        (summary.totalCredits / summary.totalCourses).toFixed(2) : 0,
      busyDays: Object.keys(timetable.getSchedule()).filter(day => 
        Object.keys(timetable.getSchedule()[day]).length > 0
      ),
      emptySlots: 50 - Object.values(timetable.getSchedule()).reduce((acc, day) => 
        acc + Object.keys(day).length, 0
      ) // Assuming 10 slots per day * 5 days
    };

    res.json({
      success: true,
      data: stats
    });
  } catch (error) {
    console.error('Error fetching timetable summary:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch timetable summary',
      message: error.message
    });
  }
});

// @route   POST /api/timetable/check-conflicts
// @desc    Check for conflicts before adding a course
// @access  Public
router.post('/check-conflicts', async (req, res) => {
  try {
    const { 
      courseCode, 
      facultyName, 
      slot, 
      userId = 'default' 
    } = req.body;

    // Validate required fields
    if (!courseCode || !facultyName || !slot) {
      return res.status(400).json({
        success: false,
        error: 'Missing required fields',
        message: 'courseCode, facultyName, and slot are required'
      });
    }

    // Find matching teacher
    const teachers = await csvUtils.getTeachersByCourse(courseCode);
    const teacher = teachers.find(t => 
      t.faculty === facultyName && t.slot === slot
    );

    if (!teacher) {
      return res.status(404).json({
        success: false,
        error: 'Teacher not found'
      });
    }

    // Check conflicts
    const timetable = getUserTimetable(userId);
    const slotTimings = teacher.getSlotTimings();
    const conflicts = timetable.checkConflicts(slotTimings);

    res.json({
      success: true,
      hasConflicts: conflicts.length > 0,
      conflicts: conflicts,
      slotTimings: slotTimings
    });
  } catch (error) {
    console.error('Error checking conflicts:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to check conflicts',
      message: error.message
    });
  }
});

// @route   GET /api/timetable/export
// @desc    Export timetable in various formats
// @access  Public
router.get('/export', (req, res) => {
  try {
    const { format = 'json', userId = 'default' } = req.query;
    const timetable = getUserTimetable(userId);
    
    switch (format.toLowerCase()) {
      case 'json':
        res.json({
          success: true,
          data: timetable.toJSON()
        });
        break;
        
      case 'csv':
        // Convert timetable to CSV format
        const courses = timetable.getCourses();
        let csvContent = 'Course Code,Course Title,Faculty,Slot,Venue,Credits,Type\n';
        courses.forEach(courseEntry => {
          const slots = courseEntry.slots.map(s => s.slot).join('+');
          csvContent += `${courseEntry.course.courseCode},${courseEntry.course.courseTitle},${courseEntry.teacher.faculty},${slots},${courseEntry.teacher.venue},${courseEntry.course.credits},${courseEntry.teacher.type}\n`;
        });
        
        res.setHeader('Content-Type', 'text/csv');
        res.setHeader('Content-Disposition', 'attachment; filename=timetable.csv');
        res.send(csvContent);
        break;
        
      default:
        res.status(400).json({
          success: false,
          error: 'Invalid format',
          message: 'Supported formats: json, csv'
        });
    }
  } catch (error) {
    console.error('Error exporting timetable:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to export timetable',
      message: error.message
    });
  }
});

module.exports = router;