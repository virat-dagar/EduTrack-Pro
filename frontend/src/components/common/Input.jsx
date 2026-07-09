import { User, Lock } from "lucide-react";
export function Input({ label, error, id, hint, ...props }) {
  const inputId = id || props.name;
  return (
    <label className="field" htmlFor={inputId}>
      <span className="field-label">{label}</span>
      <div className="input-wrapper">
  <input
    id={inputId}
    className={error ? "input input-error" : "input"}
    {...props}
  />

  {props.type === "password" ? (
    <Lock className="input-icon" size={18} />
  ) : (
    <User className="input-icon" size={18} />
  )}
</div>
      {hint ? <span className="field-hint">{hint}</span> : null}
      {error ? <span className="field-error">{error}</span> : null}
    </label>
  );
}
