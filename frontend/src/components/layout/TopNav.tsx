"use client";

import { Bell, Menu } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { ThemeToggle } from "@/components/ui/ThemeToggle";
import { SearchBar } from "@/components/ui/SearchBar";
import { Badge } from "@/components/ui/Badge";


interface TopNavProps {
  onSidebarToggle: () => void;
  isSidebarOpen: boolean;
}

export function TopNav({ onSidebarToggle, isSidebarOpen }: TopNavProps) {
  return (
    <header
      className="sticky top-0 z-30 flex h-16 items-center gap-3 border-b border-[var(--border)] bg-[var(--card)]/90 px-4 backdrop-blur-sm"
      role="banner"
    >
      {/* Mobile menu toggle */}
      <Button
        variant="ghost"
        size="icon"
        onClick={onSidebarToggle}
        aria-label={isSidebarOpen ? "Close sidebar" : "Open sidebar"}
        aria-expanded={isSidebarOpen}
        aria-controls="sidebar"
        className="lg:hidden"
      >
        <Menu className="h-5 w-5" />
      </Button>

      {/* Desktop sidebar toggle */}
      <Button
        variant="ghost"
        size="icon"
        onClick={onSidebarToggle}
        aria-label={isSidebarOpen ? "Collapse sidebar" : "Expand sidebar"}
        aria-expanded={isSidebarOpen}
        aria-controls="sidebar"
        className="hidden lg:flex"
      >
        <Menu className="h-5 w-5" />
      </Button>

      {/* Search */}
      <div className="flex-1 max-w-md">
        <SearchBar
          placeholder="Search cases, alerts…"
          aria-label="Search platform"
        />
      </div>

      <div className="ml-auto flex items-center gap-1">
        <ThemeToggle />

        {/* Notifications */}
        <div className="relative">
          <Button variant="ghost" size="icon" aria-label="View notifications (3 unread)">
            <Bell className="h-4 w-4" />
          </Button>
          <Badge
            variant="destructive"
            className="absolute -right-1 -top-1 h-4 min-w-4 px-1 text-[10px] leading-none flex items-center justify-center"
            aria-hidden="true"
          >
            3
          </Badge>
        </div>

        {/* Avatar */}
        <div
          className="ml-2 flex h-8 w-8 items-center justify-center rounded-full bg-[var(--primary)] text-xs font-bold text-[var(--primary-foreground)] cursor-pointer select-none"
          aria-label="User account"
          role="button"
          tabIndex={0}
          title="Analyst Account"
        >
          DA
        </div>
      </div>
    </header>
  );
}
