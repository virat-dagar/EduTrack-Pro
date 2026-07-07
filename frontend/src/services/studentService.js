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
  previewImport(file) {
    const formData = new FormData();
    formData.append("file", file);
    return api.post("/students/import/preview", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  commitImport(rows) {
    return api.post("/students/import/commit", { rows, import_valid_only: true });
  },
  exportStudents() {
    return api.get("/students/export", { responseType: "blob" });
  },
  update(id, payload) {
    return api.put(`/students/${id}`, payload);
  },
  remove(id) {
    return api.delete(`/students/${id}`);
  },
};
