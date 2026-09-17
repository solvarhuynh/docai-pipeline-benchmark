interface StatusBadgeProps {
  label: "SCAFFOLD" | "BASELINE" | "PLANNED" | "AVAILABLE";
}

export function StatusBadge({ label }: StatusBadgeProps) {
  return <span className={`status status-${label.toLowerCase()}`}>{label}</span>;
}
