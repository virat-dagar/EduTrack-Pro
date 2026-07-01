import api from "./api";

export const dashboardService = {
  teacher() {
    return api.get("/dashboard/teacher");
  },
  teacherCharts() {
    return api.get("/dashboard/teacher/charts");
  },
  teacherActivity() {
    return api.get("/dashboard/teacher/activity");
  },
  student() {
    return api.get("/dashboard/student");
  },
  studentCharts() {
    return api.get("/dashboard/student/charts");
  },
  studentActivity() {
    return api.get("/dashboard/student/activity");
  },
};
