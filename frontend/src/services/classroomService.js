import api from "./api";
import { compactParams } from "../utils/helpers";

export const classroomService = {
  list(params) {
    return api.get("/classrooms", { params: compactParams(params) });
  },
  get(id) {
    return api.get(`/classrooms/${id}`);
  },
  create(payload) {
    return api.post("/classrooms", payload);
  },
  update(id, payload) {
    return api.put(`/classrooms/${id}`, payload);
  },
  remove(id) {
    return api.delete(`/classrooms/${id}`);
  },
};
