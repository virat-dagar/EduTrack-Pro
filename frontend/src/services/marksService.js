import api from "./api";
import { compactParams } from "../utils/helpers";

export const marksService = {
  list(params) {
    return api.get("/marks", { params: compactParams(params) });
  },
  get(id) {
    return api.get(`/marks/${id}`);
  },
  create(payload) {
    return api.post("/marks", payload);
  },
  update(id, payload) {
    return api.put(`/marks/${id}`, payload);
  },
  remove(id) {
    return api.delete(`/marks/${id}`);
  },
  student(studentId, params) {
    return api.get(`/marks/student/${studentId}`, { params: compactParams(params) });
  },
  summary() {
    return api.get("/marks/summary");
  },
  average(studentId) {
    return api.get(`/marks/average/${studentId}`);
  },
};
