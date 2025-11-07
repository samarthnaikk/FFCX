class Course {
  constructor(data) {
    this.serialNumber = data['l.no'] || data.serialNumber;
    this.courseCode = data['Course Code'] || data.courseCode;
    this.courseTitle = data['Course Title'] || data.courseTitle;
    this.courseType = data['Course Type'] || data.courseType;
    this.version = data['Version'] || data.version;
    this.lectureHours = parseInt(data['L'] || data.lectureHours || 0);
    this.tutorialHours = parseInt(data['T'] || data.tutorialHours || 0);
    this.practicalHours = parseInt(data['P'] || data.practicalHours || 0);
    this.projectHours = parseInt(data['J'] || data.projectHours || 0);
    this.credits = parseFloat(data['Credits'] || data.credits || 0);
  }

  // Check if course is theory only
  isTheoryOnly() {
    return this.courseType === 'Theory Only';
  }

  // Check if course is lab only
  isLabOnly() {
    return this.courseType === 'Lab Only';
  }

  // Check if course has embedded theory and lab
  isEmbedded() {
    return this.courseType === 'Embedded Theory and Lab';
  }

  // Get total contact hours
  getTotalHours() {
    return this.lectureHours + this.tutorialHours + this.practicalHours + this.projectHours;
  }

  // Convert to JSON for API response
  toJSON() {
    return {
      serialNumber: this.serialNumber,
      courseCode: this.courseCode,
      courseTitle: this.courseTitle,
      courseType: this.courseType,
      version: this.version,
      lectureHours: this.lectureHours,
      tutorialHours: this.tutorialHours,
      practicalHours: this.practicalHours,
      projectHours: this.projectHours,
      credits: this.credits,
      totalHours: this.getTotalHours()
    };
  }
}

module.exports = Course;