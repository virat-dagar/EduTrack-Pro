export function EmptyState({ title = "Nothing here yet", description }) {
  return (
    <div className="state state-empty">
      <p>{title}</p>
      {description ? <span>{description}</span> : null}
    </div>
  );
}
