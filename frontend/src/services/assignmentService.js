import api from "./api";
import { compactParams } from "../utils/helpers";

export const assignmentService = {
  list(params) {
    return api.get("/assignments", { params: compactParams(params) });
  },
  get(id) {
    return api.get(`/assignments/${id}`);
  },
  upload(file) {
    const formData = new FormData();
    formData.append("file", file);
    return api.post("/assignments/upload", formData);
  },
  create(payload) {
    return api.post("/assignments", payload);
  },
  update(id, payload) {
    return api.put(`/assignments/${id}`, payload);
  },
  publish(id) {
    return api.put(`/assignments/${id}/publish`);
  },
  submissionSummary(id) {
    return api.get(`/assignments/${id}/submissions/summary`);
  },
  remove(id) {
    return api.delete(`/assignments/${id}`);
  },
  upcoming() {
    return api.get("/assignments/upcoming");
  },
  overdue() {
    return api.get("/assignments/overdue");
  },
};