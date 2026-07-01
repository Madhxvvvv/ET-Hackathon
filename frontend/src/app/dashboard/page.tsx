import type { Metadata } from "next";
import { ScanLine, Network, ShieldCheck, AlertTriangle } from "lucide-react";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { StatCard } from "@/components/ui/StatCard";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Alert } from "@/components/ui/Alert";

export const metadata: Metadata = { title: "Dashboard" };

const stats = [
  { label: "Notes Scanned Today", value: "1,247", change: 12, trend: "up" as const, icon: ScanLine },
  { label: "Fraud Cases Detected", value: "34", change: -5, trend: "down" as const, icon: Network },
  { label: "Scam Alerts Issued", value: "89", change: 8, trend: "up" as const, icon: ShieldCheck },
  { label: "Active Investigations", value: "12", trend: "neutral" as const, icon: AlertTriangle },
];

const recentAlerts = [
  { id: 1, type: "Counterfeit", description: "₹500 note flagged — Nehru Nagar, Delhi", severity: "error" as const, time: "2 min ago" },
  { id: 2, type: "Fraud Network", description: "New mule account cluster identified — 14 nodes", severity: "warning" as const, time: "18 min ago" },
  { id: 3, type: "Scam Shield", description: "Digital arrest impersonation pattern detected", severity: "warning" as const, time: "1 hr ago" },
  { id: 4, type: "Counterfeit", description: "₹2000 note flagged — MG Road, Bengaluru", severity: "error" as const, time: "3 hr ago" },
];

const severityBadge: Record<string, "destructive" | "warning" | "info"> = {
  error: "destructive",
  warning: "warning",
  info: "info",
};

export default function DashboardPage() {
  return (
    <DashboardLayout>
      <PageHeader
        title="Overview"
        description="Real-time summary of platform activity across all modules."
        breadcrumbs={[{ label: "Dashboard" }]}
      />

      <Alert variant="info" title="API Integration Pending" className="mb-6">
        Data shown is placeholder. Live API integration will be completed in Day 2.
      </Alert>

      {/* Stats */}
      <section aria-label="Statistics" className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => (
          <StatCard key={stat.label} {...stat} changeLabel="vs yesterday" />
        ))}
      </section>

      {/* Recent Alerts */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Recent Alerts</CardTitle>
            <CardDescription>Latest detections across all modules</CardDescription>
          </CardHeader>
          <CardContent className="p-0">
            <ul role="list" className="divide-y divide-[var(--border)]">
              {recentAlerts.map((alert) => (
                <li key={alert.id} className="flex items-center justify-between gap-4 px-6 py-4">
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2">
                      <Badge variant={severityBadge[alert.severity]}>{alert.type}</Badge>
                    </div>
                    <p className="mt-1 text-sm text-[var(--foreground)]">{alert.description}</p>
                  </div>
                  <span className="shrink-0 text-xs text-[var(--muted-foreground)]">{alert.time}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Module Status</CardTitle>
            <CardDescription>Current operational status</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {[
              { name: "Currency Scanner", status: "API Pending", color: "warning" as const },
              { name: "Fraud Network", status: "API Pending", color: "warning" as const },
              { name: "Scam Shield", status: "RAG Live", color: "success" as const },
              { name: "Backend Gateway", status: "Scaffolded", color: "secondary" as const },
            ].map(({ name, status, color }) => (
              <div key={name} className="flex items-center justify-between">
                <span className="text-sm">{name}</span>
                <Badge variant={color}>{status}</Badge>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
