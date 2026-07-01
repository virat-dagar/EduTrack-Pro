import api from "./api";

export const reportService = {
  student(studentId) {
    return api.get(`/reports/student/${studentId}`);
  },
  attendance() {
    return api.get("/reports/attendance");
  },
  marks() {
    return api.get("/reports/marks");
  },
  assignments() {
    return api.get("/reports/assignments");
  },
  performance() {
    return api.get("/reports/performance");
  },
  institution() {
    return api.get("/reports/institution");
  },
};
