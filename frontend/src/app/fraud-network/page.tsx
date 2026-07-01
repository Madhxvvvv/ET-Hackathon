import type { Metadata } from "next";
import { Network } from "lucide-react";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card";
import { Alert } from "@/components/ui/Alert";
import { Badge } from "@/components/ui/Badge";
import { StatCard } from "@/components/ui/StatCard";
import { EmptyState } from "@/components/ui/EmptyState";

export const metadata: Metadata = { title: "Fraud Network" };

const placeholderNodes = [
  { id: "ACC-001", type: "Mule Account", risk: "High", connections: 14, flagged: true },
  { id: "ACC-002", type: "Primary Account", risk: "Medium", connections: 6, flagged: false },
  { id: "ACC-003", type: "Mule Account", risk: "High", connections: 9, flagged: true },
  { id: "ACC-004", type: "Shell Entity", risk: "Critical", connections: 22, flagged: true },
  { id: "ACC-005", type: "Beneficiary", risk: "Low", connections: 2, flagged: false },
];

const riskBadge: Record<string, "destructive" | "warning" | "secondary" | "default"> = {
  Critical: "destructive",
  High: "destructive",
  Medium: "warning",
  Low: "secondary",
};

export default function FraudNetworkPage() {
  return (
    <DashboardLayout>
      <PageHeader
        title="Fraud Network Intelligence"
        description="Graph-based analysis to expose fraud networks and mule account clusters."
        breadcrumbs={[{ label: "Dashboard", href: "/dashboard" }, { label: "Fraud Network" }]}
      />

      <Alert variant="warning" title="Module Under Development" className="mb-6">
        Neo4j graph database integration is pending. Network visualisation will be available in Day 2.
      </Alert>

      <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
        <StatCard label="Nodes in Graph" value="2,847" trend="up" change={3} changeLabel="this week" />
        <StatCard label="Flagged Accounts" value="341" trend="up" change={11} changeLabel="this week" />
        <StatCard label="Active Clusters" value="18" trend="neutral" />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Graph placeholder */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Network Graph</CardTitle>
            <CardDescription>Interactive D3/Cytoscape graph visualisation — Day 2</CardDescription>
          </CardHeader>
          <CardContent>
            <EmptyState
              title="Graph not yet connected"
              description="Neo4j API integration and D3.js visualisation will be implemented in Day 2."
              icon={<Network className="h-8 w-8 text-[var(--muted-foreground)]" />}
            />
          </CardContent>
        </Card>

        {/* Node list */}
        <Card>
          <CardHeader>
            <CardTitle>Flagged Nodes</CardTitle>
            <CardDescription>Accounts under investigation</CardDescription>
          </CardHeader>
          <CardContent className="p-0">
            <ul role="list" className="divide-y divide-[var(--border)]">
              {placeholderNodes.map((node) => (
                <li key={node.id} className="flex items-center justify-between px-6 py-3">
                  <div>
                    <p className="text-sm font-mono font-medium">{node.id}</p>
                    <p className="text-xs text-[var(--muted-foreground)]">{node.type} · {node.connections} links</p>
                  </div>
                  <Badge variant={riskBadge[node.risk]}>{node.risk}</Badge>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
