export function formatPercent(value) {
  const number = Number(value || 0);
  return `${number.toFixed(1)}%`;
}

export function formatNumber(value) {
  return new Intl.NumberFormat("en").format(Number(value || 0));
}

export function humanize(value) {
  return String(value || "")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}
