export const ROLES = {
  TEACHER: "teacher",
  STUDENT: "student",
};

export const ROUTES = {
  LOGIN: "/login",
  TEACHER_DASHBOARD: "/dashboard/teacher",
  STUDENT_DASHBOARD: "/dashboard/student",
  FORBIDDEN: "/forbidden",
};

export const STORAGE_KEYS = {
  TOKEN: "access_token",
  USER: "current_user",
  THEME: "theme",
  SIDEBAR: "sidebar_collapsed",
};

export const ASSESSMENT_TYPES = [
  "Assignment",
  "Quiz",
  "Internal",
  "Mid Semester",
  "Practical",
  "End Semester",
];

export const ATTENDANCE_STATUSES = ["Present", "Absent", "Late"];

export const SUBMISSION_STATUSES = ["Pending", "Submitted", "Late", "Reviewed"];
