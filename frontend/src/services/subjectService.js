import api from "./api";
import { compactParams } from "../utils/helpers";

export const subjectService = {
  list(params) {
    return api.get("/subjects", { params: compactParams(params) });
  },
  search(params) {
    return api.get("/subjects/search", { params: compactParams(params) });
  },
  get(id) {
    return api.get(`/subjects/${id}`);
  },
  create(payload) {
    return api.post("/subjects", payload);
  },
  update(id, payload) {
    return api.put(`/subjects/${id}`, payload);
  },
  remove(id) {
    return api.delete(`/subjects/${id}`);
  },
};
