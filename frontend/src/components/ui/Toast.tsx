"use client";

import { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";
import { CheckCircle2, AlertCircle, AlertTriangle, X, Info } from "lucide-react";
import { cn } from "@/lib/utils";
import type { ToastMessage, ToastVariant } from "@/types";

/* ─── Context ─────────────────────────────────────────────────────────── */

interface ToastContextValue {
  toast: (msg: Omit<ToastMessage, "id">) => void;
  dismiss: (id: string) => void;
}

const ToastContext = createContext<ToastContextValue | null>(null);

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error("useToast must be used inside <ToastProvider>");
  return ctx;
}

/* ─── Individual Toast ─────────────────────────────────────────────────── */

const variantConfig: Record<ToastVariant, { icon: typeof Info; className: string }> = {
  default: { icon: Info, className: "border-[var(--border)] bg-[var(--card)]" },
  success: { icon: CheckCircle2, className: "border-emerald-200 bg-emerald-50 dark:border-emerald-800 dark:bg-emerald-950/30" },
  error: { icon: AlertCircle, className: "border-red-200 bg-red-50 dark:border-red-800 dark:bg-red-950/30" },
  warning: { icon: AlertTriangle, className: "border-amber-200 bg-amber-50 dark:border-amber-800 dark:bg-amber-950/30" },
};

function ToastItem({ toast, onDismiss }: { toast: ToastMessage; onDismiss: (id: string) => void }) {
  const config = variantConfig[toast.variant ?? "default"];
  const { icon: Icon } = config;

  useEffect(() => {
    const timer = setTimeout(() => onDismiss(toast.id), toast.duration ?? 5000);
    return () => clearTimeout(timer);
  }, [toast.id, toast.duration, onDismiss]);

  return (
    <div
      role="alert"
      aria-live="polite"
      className={cn(
        "flex w-full max-w-sm items-start gap-3 rounded-xl border p-4 shadow-lg",
        "animate-in slide-in-from-right-4 fade-in-0 duration-300",
        config.className
      )}
    >
      <Icon className="mt-0.5 h-5 w-5 shrink-0" aria-hidden="true" />
      <div className="flex-1 min-w-0">
        <p className="text-sm font-semibold">{toast.title}</p>
        {toast.description && (
          <p className="mt-0.5 text-sm text-[var(--muted-foreground)]">{toast.description}</p>
        )}
      </div>
      <button
        onClick={() => onDismiss(toast.id)}
        aria-label="Dismiss notification"
        className="shrink-0 rounded p-0.5 text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  );
}

/* ─── Provider ─────────────────────────────────────────────────────────── */

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);
  const counterRef = useRef(0);

  const toast = useCallback((msg: Omit<ToastMessage, "id">) => {
    const id = `toast-${++counterRef.current}`;
    setToasts((prev) => [...prev, { ...msg, id }]);
  }, []);

  const dismiss = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ toast, dismiss }}>
      {children}
      <div
        aria-label="Notifications"
        className="fixed bottom-4 right-4 z-50 flex flex-col gap-2"
      >
        {toasts.map((t) => (
          <ToastItem key={t.id} toast={t} onDismiss={dismiss} />
        ))}
      </div>
    </ToastContext.Provider>
  );
}
