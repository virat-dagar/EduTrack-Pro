const STORAGE_PREFIX = "edutrack_pro";

export const storage = {
  get(key) {
    return window.localStorage.getItem(`${STORAGE_PREFIX}:${key}`);
  },
  set(key, value) {
    window.localStorage.setItem(`${STORAGE_PREFIX}:${key}`, value);
  },
  remove(key) {
    window.localStorage.removeItem(`${STORAGE_PREFIX}:${key}`);
  },
  getJson(key) {
    const value = storage.get(key);
    return value ? JSON.parse(value) : null;
  },
  setJson(key, value) {
    storage.set(key, JSON.stringify(value));
  },
};
