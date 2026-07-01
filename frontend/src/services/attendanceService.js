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
