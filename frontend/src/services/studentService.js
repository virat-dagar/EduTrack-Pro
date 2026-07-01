import api from "./api";
import { compactParams } from "../utils/helpers";

export const studentService = {
  list(params) {
    return api.get("/students", { params: compactParams(params) });
  },
  search(params) {
    return api.get("/students/search", { params: compactParams(params) });
  },
  me() {
    return api.get("/students/me");
  },
  get(id) {
    return api.get(`/students/${id}`);
  },
  create(payload) {
    return api.post("/students", payload);
  },
  update(id, payload) {
    return api.put(`/students/${id}`, payload);
  },
  remove(id) {
    return api.delete(`/students/${id}`);
  },
};
