import { X } from "lucide-react";
import { Button } from "./Button";

export function Modal({ isOpen, title, children, onClose }) {
  if (!isOpen) return null;
  return (
    <div className="modal-backdrop" role="presentation">
      <section className="modal" role="dialog" aria-modal="true" aria-label={title}>
        <header className="modal-header">
          <h2>{title}</h2>
          <Button variant="ghost" size="icon" icon={X} onClick={onClose} aria-label="Close dialog" />
        </header>
        <div className="modal-body">{children}</div>
      </section>
    </div>
  );
}
