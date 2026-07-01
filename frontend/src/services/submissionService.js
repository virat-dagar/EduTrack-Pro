import api from "./api";
import { compactParams } from "../utils/helpers";

export const submissionService = {
  list(params) {
    return api.get("/submissions", { params: compactParams(params) });
  },
  get(id) {
    return api.get(`/submissions/${id}`);
  },
  create(payload) {
    return api.post("/submissions", payload);
  },
  update(id, payload) {
    return api.put(`/submissions/${id}`, payload);
  },
  remove(id) {
    return api.delete(`/submissions/${id}`);
  },
  review(id, payload) {
    return api.put(`/submissions/${id}/review`, payload);
  },
  pending() {
    return api.get("/submissions/pending");
  },
};
