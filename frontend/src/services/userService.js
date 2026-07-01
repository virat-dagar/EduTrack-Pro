import api from "./api";
import { compactParams } from "../utils/helpers";

export const userService = {
  list(params) {
    return api.get("/users", { params: compactParams(params) });
  },
  get(id) {
    return api.get(`/users/${id}`);
  },
  create(payload) {
    return api.post("/users", payload);
  },
  update(id, payload) {
    return api.put(`/users/${id}`, payload);
  },
  remove(id) {
    return api.delete(`/users/${id}`);
  },
  activate(id) {
    return api.put(`/users/${id}/activate`);
  },
  deactivate(id) {
    return api.put(`/users/${id}/deactivate`);
  },
};
