import { ROLES, ROUTES } from "./constants";

export function getDashboardPath(user) {
  if (user?.role === ROLES.STUDENT) return ROUTES.STUDENT_DASHBOARD;
  return ROUTES.TEACHER_DASHBOARD;
}

export function unwrap(response) {
  return response?.data ?? response;
}

export function compactParams(params) {
  return Object.fromEntries(
    Object.entries(params || {}).filter(([, value]) => value !== "" && value !== null && value !== undefined),
  );
}
