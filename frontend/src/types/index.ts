export type NavItem = {
  label: string;
  href: string;
  icon?: React.ComponentType<{ className?: string }>;
  badge?: string | number;
};

export type BreadcrumbItem = {
  label: string;
  href?: string;
};

export type StatCardData = {
  label: string;
  value: string | number;
  change?: number;
  changeLabel?: string;
  icon?: React.ComponentType<{ className?: string }>;
  trend?: "up" | "down" | "neutral";
};

export type AlertVariant = "info" | "success" | "warning" | "error";

export type ToastVariant = "default" | "success" | "error" | "warning";

export interface ToastMessage {
  id: string;
  title: string;
  description?: string;
  variant?: ToastVariant;
  duration?: number;
}
