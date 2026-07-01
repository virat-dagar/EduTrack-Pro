import { AlertTriangle } from "lucide-react";

export function ErrorState({ title = "Something went wrong", message }) {
  return (
    <div className="state state-error" role="alert">
      <AlertTriangle size={24} aria-hidden="true" />
      <p>{title}</p>
      {message ? <span>{message}</span> : null}
    </div>
  );
}
