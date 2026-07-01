import { Shield } from "lucide-react";
import { APP_VERSION } from "@/constants/navigation";

export function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="border-t border-[var(--border)] bg-[var(--card)] px-6 py-4" role="contentinfo">
      <div className="flex flex-col items-center justify-between gap-2 sm:flex-row">
        <div className="flex items-center gap-2 text-sm text-[var(--muted-foreground)]">
          <Shield className="h-4 w-4 text-[var(--primary)]" aria-hidden="true" />
          <span>Digital Public Safety Platform</span>
          <span aria-hidden="true">·</span>
          <span>v{APP_VERSION}</span>
        </div>
        <p className="text-sm text-[var(--muted-foreground)]">
          © {year} ET AI Hackathon 2026. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
