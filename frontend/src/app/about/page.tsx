import type { Metadata } from "next";
import { Shield, Users, GitBranch } from "lucide-react";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

export const metadata: Metadata = { title: "About" };

const team = [
  { name: "Person 1", role: "ML Engineer", module: "Counterfeit Detection", stack: "PyTorch · EfficientNet" },
  { name: "Person 2", role: "Backend Engineer", module: "Fraud Network", stack: "FastAPI · Neo4j" },
  { name: "Person 3", role: "Frontend Engineer", module: "Unified Dashboard", stack: "Next.js · Tailwind" },
  { name: "Person 4", role: "RAG Engineer", module: "Scam Shield", stack: "LangChain · ChromaDB" },
];

const techStack = [
  { category: "Frontend", items: ["Next.js 16", "React 19", "TypeScript", "Tailwind CSS", "Lucide Icons"] },
  { category: "Backend", items: ["FastAPI", "PostgreSQL", "Neo4j", "Python 3.12"] },
  { category: "ML / RAG", items: ["EfficientNet-B0", "Albumentations", "LangChain", "ChromaDB", "sentence-transformers"] },
  { category: "DevOps", items: ["Render", "Vercel", "GitHub Actions"] },
];

export default function AboutPage() {
  return (
    <DashboardLayout>
      <PageHeader
        title="About"
        description="Digital Public Safety Platform — ET AI Hackathon 2026"
        breadcrumbs={[{ label: "Dashboard", href: "/dashboard" }, { label: "About" }]}
      />

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-3">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5 text-[var(--primary)]" aria-hidden="true" />
              Project Overview
            </CardTitle>
          </CardHeader>
          <CardContent className="prose prose-sm max-w-none text-[var(--foreground)]">
            <p>
              The <strong>Digital Public Safety Platform</strong> is an AI-powered system built for the
              ET AI Hackathon 2026 under the theme <em>&quot;AI for Digital Public Safety: Defeating Counterfeiting,
              Fraud &amp; Digital Arrest Scams.&quot;</em>
            </p>
            <p className="mt-2 text-[var(--muted-foreground)]">
              The platform unifies four independently developed AI modules into a single dashboard:
              counterfeit currency detection (EfficientNet), fraud network intelligence (Neo4j graph analysis),
              and a scam shield chatbot grounded in official CERT-In and RBI advisories (RAG pipeline).
            </p>
          </CardContent>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="h-5 w-5 text-[var(--primary)]" aria-hidden="true" />
              Team
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {team.map(({ name, role, module, stack }) => (
              <div key={name} className="flex items-center gap-4">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[var(--accent)] text-sm font-bold text-[var(--accent-foreground)]">
                  {name.split(" ")[0][0]}{name.split(" ")[1]?.[0]}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium">{name} <span className="text-[var(--muted-foreground)] font-normal">— {role}</span></p>
                  <p className="text-sm text-[var(--muted-foreground)]">{module} · <span className="font-mono text-xs">{stack}</span></p>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <GitBranch className="h-5 w-5 text-[var(--primary)]" aria-hidden="true" />
              Tech Stack
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {techStack.map(({ category, items }) => (
              <div key={category}>
                <p className="mb-1.5 text-xs font-semibold uppercase tracking-wider text-[var(--muted-foreground)]">{category}</p>
                <div className="flex flex-wrap gap-1.5">
                  {items.map((item) => (
                    <Badge key={item} variant="secondary">{item}</Badge>
                  ))}
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
