"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard, ScanLine, Network, ShieldCheck,
  Settings, Info, Shield, X,
} from "lucide-react";
import { cn } from "@/lib/utils";


const iconMap = {
  LayoutDashboard,
  ScanLine,
  Network,
  ShieldCheck,
  Settings,
  Info,
} as const;

const navItems = [
  { label: "Dashboard", href: "/dashboard", icon: "LayoutDashboard" as const },
  { label: "Currency Scanner", href: "/scanner", icon: "ScanLine" as const },
  { label: "Fraud Network", href: "/fraud-network", icon: "Network" as const },
  { label: "Scam Shield", href: "/scam-shield", icon: "ShieldCheck" as const },
  { label: "Settings", href: "/settings", icon: "Settings" as const },
  { label: "About", href: "/about", icon: "Info" as const },
];

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  className?: string;
}

export function Sidebar({ isOpen, onClose, className }: SidebarProps) {
  const pathname = usePathname();

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      <aside
        id="sidebar"
        aria-label="Main navigation"
        className={cn(
          "fixed left-0 top-0 z-50 flex h-full w-64 flex-col bg-[var(--sidebar)] text-[var(--sidebar-foreground)] transition-transform duration-300",
          "lg:relative lg:z-auto lg:translate-x-0",
          isOpen ? "translate-x-0" : "-translate-x-full",
          className
        )}
      >
        {/* Logo */}
        <div className="flex items-center justify-between px-4 py-5 border-b border-white/10">
          <Link href="/" className="flex items-center gap-3 group" aria-label="Home">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-500 shadow-sm">
              <Shield className="h-5 w-5 text-white" aria-hidden="true" />
            </div>
            <div className="leading-tight">
              <p className="text-xs font-bold text-white uppercase tracking-wider">DPSP</p>
              <p className="text-[10px] text-white/60 leading-tight">Public Safety</p>
            </div>
          </Link>
          <button
            onClick={onClose}
            aria-label="Close sidebar"
            className="rounded-md p-1.5 text-white/60 hover:text-white hover:bg-white/10 lg:hidden"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {/* Nav */}
        <nav className="flex flex-1 flex-col gap-1 overflow-y-auto px-3 py-4">
          <p className="mb-2 px-2 text-[10px] font-semibold uppercase tracking-widest text-white/40">
            Navigation
          </p>
          {navItems.map(({ label, href, icon }) => {
            const Icon = iconMap[icon];
            const isActive = pathname === href || pathname.startsWith(`${href}/`);
            return (
              <Link
                key={href}
                href={href}
                aria-current={isActive ? "page" : undefined}
                className={cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-400",
                  isActive
                    ? "bg-blue-600 text-white shadow-sm"
                    : "text-white/70 hover:bg-white/10 hover:text-white"
                )}
              >
                <Icon className="h-4 w-4 shrink-0" aria-hidden="true" />
                {label}
              </Link>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="border-t border-white/10 px-4 py-4">
          <p className="text-[10px] text-white/40 leading-tight">
            Digital Public Safety Platform
            <br />
            v1.0.0 · ET AI Hackathon 2026
          </p>
        </div>
      </aside>
    </>
  );
}
