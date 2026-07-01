"use client";

import { useSidebar } from "@/hooks/useSidebar";
import { Sidebar } from "./Sidebar";
import { TopNav } from "./TopNav";
import { Footer } from "./Footer";
import { cn } from "@/lib/utils";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const { isOpen, toggle } = useSidebar(true);

  return (
    <div className="flex h-screen overflow-hidden bg-[var(--background)]">
      <Sidebar isOpen={isOpen} onClose={toggle} />

      <div className="flex flex-1 flex-col overflow-hidden">
        <TopNav onSidebarToggle={toggle} isSidebarOpen={isOpen} />
        <main
          id="main-content"
          className={cn(
            "flex-1 overflow-y-auto",
            "transition-all duration-300"
          )}
          tabIndex={-1}
        >
          <div className="px-6 py-6">
            {children}
          </div>
        </main>
        <Footer />
      </div>
    </div>
  );
}
