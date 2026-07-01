export function isEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

export function required(value) {
  return value !== undefined && value !== null && String(value).trim() !== "";
}

export function validateLogin(values) {
  const errors = {};
  if (!required(values.email)) errors.email = "Email is required.";
  if (values.email && !isEmail(values.email)) errors.email = "Enter a valid email.";
  if (!required(values.password)) errors.password = "Password is required.";
  return errors;
}
