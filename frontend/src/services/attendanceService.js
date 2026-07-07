import api from "./api";
import { compactParams } from "../utils/helpers";

export const attendanceService = {
  list(params) {
    return api.get("/attendance", { params: compactParams(params) });
  },
  get(id) {
    return api.get(`/attendance/${id}`);
  },
  create(payload) {
    return api.post("/attendance", payload);
  },
  bulk(payload) {
    return api.post("/attendance/bulk", payload);
  },
  sheet(classroomId, params) {
    return api.get(`/attendance/classroom/${classroomId}/sheet`, { params: compactParams(params) });
  },
  analytics(params) {
    return api.get("/attendance/analytics", { params: compactParams(params) });
  },
  atRisk(params) {
    return api.get("/attendance/at-risk", { params: compactParams(params) });
  },
  update(id, payload) {
    return api.put(`/attendance/${id}`, payload);
  },
  remove(id) {
    return api.delete(`/attendance/${id}`);
  },
  student(studentId, params) {
    return api.get(`/attendance/student/${studentId}`, { params: compactParams(params) });
  },
  summary() {
    return api.get("/attendance/summary");
  },
  percentage(studentId) {
    return api.get(`/attendance/percentage/${studentId}`);
  },
};
