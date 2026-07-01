export function formatDate(value) {
  if (!value) return "-";
  return new Intl.DateTimeFormat("en", {
    year: "numeric",
    month: "short",
    day: "numeric",
  }).format(new Date(value));
}

export function todayISO() {
  return new Date().toISOString().slice(0, 10);
}
