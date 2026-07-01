export function Button({
  children,
  type = "button",
  variant = "primary",
  size = "md",
  icon: Icon,
  isLoading = false,
  className = "",
  ...props
}) {
  return (
    <button
      type={type}
      className={`btn btn-${variant} btn-${size} ${className}`}
      disabled={isLoading || props.disabled}
      {...props}
    >
      {Icon ? <Icon size={18} aria-hidden="true" /> : null}
      <span>{isLoading ? "Please wait" : children}</span>
    </button>
  );
}
