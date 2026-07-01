import axios from "axios";
import { STORAGE_KEYS } from "../utils/constants";
import { storage } from "../utils/storage";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = storage.get(STORAGE_KEYS.TOKEN);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const status = error.response?.status;
    const payload = error.response?.data || {
      success: false,
      message: "Network error. Please try again.",
      errors: [],
    };
    if (status === 401) {
      window.dispatchEvent(new Event("edutrack:unauthorized"));
    }
    return Promise.reject(payload);
  },
);

export default api;
