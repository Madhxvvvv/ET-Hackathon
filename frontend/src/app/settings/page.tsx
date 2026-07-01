import type { Metadata } from "next";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card";
import { Alert } from "@/components/ui/Alert";

export const metadata: Metadata = { title: "Settings" };

const settingsSections = [
  {
    title: "API Configuration",
    description: "Backend service endpoints and authentication.",
    fields: [
      { label: "Backend API URL", placeholder: "http://localhost:8000/api/v1", type: "url" },
      { label: "RAG Service URL", placeholder: "http://localhost:8001", type: "url" },
    ],
  },
  {
    title: "Notification Preferences",
    description: "Configure alert thresholds and notification channels.",
    fields: [
      { label: "Alert Email", placeholder: "analyst@dpsp.gov.in", type: "email" },
      { label: "Confidence Threshold (%)", placeholder: "85", type: "number" },
    ],
  },
];

export default function SettingsPage() {
  return (
    <DashboardLayout>
      <PageHeader
        title="Settings"
        description="Configure platform behaviour, API endpoints, and preferences."
        breadcrumbs={[{ label: "Dashboard", href: "/dashboard" }, { label: "Settings" }]}
      />

      <Alert variant="info" title="Settings Not Persisted" className="mb-6">
        Settings persistence will be implemented in Day 2 with a backend user preferences API.
      </Alert>

      <div className="space-y-6 max-w-2xl">
        {settingsSections.map(({ title, description, fields }) => (
          <Card key={title}>
            <CardHeader>
              <CardTitle>{title}</CardTitle>
              <CardDescription>{description}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {fields.map(({ label, placeholder, type }) => (
                <div key={label}>
                  <label
                    htmlFor={label.toLowerCase().replace(/\s+/g, "-")}
                    className="mb-1.5 block text-sm font-medium"
                  >
                    {label}
                  </label>
                  <input
                    id={label.toLowerCase().replace(/\s+/g, "-")}
                    type={type}
                    placeholder={placeholder}
                    disabled
                    className="w-full rounded-lg border border-[var(--input)] bg-[var(--background)] px-3 py-2 text-sm placeholder:text-[var(--muted-foreground)] disabled:opacity-50 focus:border-[var(--ring)] focus:outline-none focus:ring-2 focus:ring-[var(--ring)]/20"
                  />
                </div>
              ))}
            </CardContent>
          </Card>
        ))}
      </div>
    </DashboardLayout>
  );
}
