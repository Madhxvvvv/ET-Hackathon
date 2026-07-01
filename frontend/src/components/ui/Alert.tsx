import { cn } from "@/lib/utils";
import { AlertCircle, CheckCircle2, Info, AlertTriangle } from "lucide-react";
import type { AlertVariant } from "@/types";

interface AlertProps {
  variant?: AlertVariant;
  title?: string;
  children: React.ReactNode;
  className?: string;
}

const variantConfig = {
  info: {
    containerClass: "bg-blue-50 border-blue-200 dark:bg-blue-950/30 dark:border-blue-800",
    iconClass: "text-blue-600 dark:text-blue-400",
    Icon: Info,
  },
  success: {
    containerClass: "bg-emerald-50 border-emerald-200 dark:bg-emerald-950/30 dark:border-emerald-800",
    iconClass: "text-emerald-600 dark:text-emerald-400",
    Icon: CheckCircle2,
  },
  warning: {
    containerClass: "bg-amber-50 border-amber-200 dark:bg-amber-950/30 dark:border-amber-800",
    iconClass: "text-amber-600 dark:text-amber-400",
    Icon: AlertTriangle,
  },
  error: {
    containerClass: "bg-red-50 border-red-200 dark:bg-red-950/30 dark:border-red-800",
    iconClass: "text-red-600 dark:text-red-400",
    Icon: AlertCircle,
  },
};

export function Alert({ variant = "info", title, children, className }: AlertProps) {
  const config = variantConfig[variant];
  const { Icon } = config;

  return (
    <div
      role="alert"
      className={cn("flex gap-3 rounded-lg border p-4", config.containerClass, className)}
    >
      <Icon className={cn("mt-0.5 h-5 w-5 shrink-0", config.iconClass)} aria-hidden="true" />
      <div className="flex-1 text-sm">
        {title && <p className="mb-1 font-semibold">{title}</p>}
        <div className="text-[var(--foreground)]/80">{children}</div>
      </div>
    </div>
  );
}
