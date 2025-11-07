const express = require('express');
const csvUtils = require('../utils/csvUtils');
const router = express.Router();

// @route   GET /api/courses
// @desc    Get all courses or search courses
// @access  Public
router.get('/', async (req, res) => {
  try {
    const { search, type, limit = 50 } = req.query;
    
    let courses;
    if (search) {
      courses = await csvUtils.searchCourses(search);
    } else {
      courses = await csvUtils.loadCourses();
    }

    // Filter by course type if specified
    if (type) {
      courses = courses.filter(course => 
        course.courseType.toLowerCase().includes(type.toLowerCase())
      );
    }

    // Apply limit
    const limitNum = parseInt(limit);
    if (limitNum > 0 && courses.length > limitNum) {
      courses = courses.slice(0, limitNum);
    }

    res.json({
      success: true,
      count: courses.length,
      data: courses.map(course => course.toJSON())
    });
  } catch (error) {
    console.error('Error fetching courses:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch courses',
      message: error.message
    });
  }
});

// @route   GET /api/courses/:courseCode
// @desc    Get specific course by course code
// @access  Public
router.get('/:courseCode', async (req, res) => {
  try {
    const { courseCode } = req.params;
    const course = await csvUtils.getCourseByCode(courseCode);
    
    if (!course) {
      return res.status(404).json({
        success: false,
        error: 'Course not found',
        message: `No course found with code: ${courseCode}`
      });
    }

    res.json({
      success: true,
      data: course.toJSON()
    });
  } catch (error) {
    console.error('Error fetching course:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch course',
      message: error.message
    });
  }
});

// @route   GET /api/courses/search/autocomplete
// @desc    Get courses for autocomplete (optimized for frontend)
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

    const courses = await csvUtils.searchCourses(q);
    const limitNum = parseInt(limit);
    const limitedCourses = courses.slice(0, limitNum);

    // Return simplified data for autocomplete
    const autocompleteData = limitedCourses.map(course => ({
      courseCode: course.courseCode,
      courseTitle: course.courseTitle,
      courseType: course.courseType,
      credits: course.credits,
      label: `${course.courseCode} - ${course.courseTitle}`,
      value: course.courseCode
    }));

    res.json({
      success: true,
      count: autocompleteData.length,
      data: autocompleteData
    });
  } catch (error) {
    console.error('Error in autocomplete search:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to perform autocomplete search',
      message: error.message
    });
  }
});

// @route   GET /api/courses/stats
// @desc    Get course statistics
// @access  Public
router.get('/admin/stats', async (req, res) => {
  try {
    const stats = await csvUtils.getDataStats();
    res.json({
      success: true,
      data: stats
    });
  } catch (error) {
    console.error('Error fetching course stats:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch course statistics',
      message: error.message
    });
  }
});

// @route   POST /api/courses/reload
// @desc    Reload course data from CSV
// @access  Public (should be protected in production)
router.post('/admin/reload', async (req, res) => {
  try {
    const stats = await csvUtils.reloadData();
    res.json({
      success: true,
      message: 'Course data reloaded successfully',
      data: stats
    });
  } catch (error) {
    console.error('Error reloading course data:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to reload course data',
      message: error.message
    });
  }
});

module.exports = router;