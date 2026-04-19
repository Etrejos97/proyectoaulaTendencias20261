export const STATUS_COLS = [
  { value: "pending",     label: "Pendiente",  color: "#f59e0b" },
  { value: "in_progress", label: "En Progreso", color: "#3b82f6" },
  { value: "in_review",   label: "En Revisión", color: "#a855f7" },
  { value: "completed",   label: "Completada",  color: "#22c55e" },
];

export const PRIORITY_MAP = {
  low:      { label: "Baja",    color: "#6b7280" },
  medium:   { label: "Media",   color: "#f59e0b" },
  high:     { label: "Alta",    color: "#ef4444" },
  critical: { label: "Crítica", color: "#dc2626" },
};

export const ROLE_OPTIONS = [
  { value: "owner",    label: "Propietario" },
  { value: "editor",   label: "Editor" },
  { value: "observer", label: "Observador" },
];