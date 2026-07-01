import type { Metadata } from "next";
import { ShieldCheck, Send, BookOpen } from "lucide-react";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card";
import { Alert } from "@/components/ui/Alert";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";

export const metadata: Metadata = { title: "Scam Shield" };

const sampleQuestions = [
  "Is it legal for police to arrest me digitally?",
  "I received a call from 'CBI' — is this real?",
  "What should I do if someone asks for OTP over phone?",
  "How can I verify if a UPI refund request is genuine?",
];

const sources = [
  { name: "CERT-In Advisory", type: "Official", category: "Digital Arrest" },
  { name: "RBI Consumer Guide", type: "Official", category: "UPI Fraud" },
  { name: "Cybercrime.gov.in", type: "Official", category: "OTP Scam" },
  { name: "MHA Digital Safety", type: "Official", category: "Impersonation" },
];

export default function ScamShieldPage() {
  return (
    <DashboardLayout>
      <PageHeader
        title="Scam Shield"
        description="RAG-powered assistant grounded in official CERT-In and RBI advisories."
        breadcrumbs={[{ label: "Dashboard", href: "/dashboard" }, { label: "Scam Shield" }]}
      />

      <Alert variant="info" title="Knowledge Base Active" className="mb-6">
        The RAG module (LangChain + ChromaDB) is live with sample documents. Chatbot UI integration is Day 2.
      </Alert>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Chat area */}
        <Card className="lg:col-span-2 flex flex-col">
          <CardHeader>
            <CardTitle>Ask the Shield</CardTitle>
            <CardDescription>Grounded answers from verified government advisories</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-1 flex-col gap-4">
            {/* Sample messages */}
            <div className="flex-1 rounded-lg bg-[var(--muted)] p-4 min-h-64">
              <div className="flex justify-end mb-4">
                <div className="max-w-xs rounded-xl rounded-tr-sm bg-[var(--primary)] px-4 py-3 text-sm text-white">
                  Is it legal for police to arrest me over a video call?
                </div>
              </div>
              <div className="flex gap-3">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-[var(--accent)]">
                  <ShieldCheck className="h-4 w-4 text-[var(--accent-foreground)]" aria-hidden="true" />
                </div>
                <div className="max-w-sm rounded-xl rounded-tl-sm bg-[var(--card)] border border-[var(--border)] px-4 py-3 text-sm">
                  <p>No. According to CERT-In Advisory CA-2024-01, no legitimate law enforcement agency in India conducts arrests via video calls. This is a known scam pattern called &ldquo;Digital Arrest.&rdquo;</p>
                  <p className="mt-2 text-xs text-[var(--muted-foreground)]">Source: CERT-In Advisory · cybercrime.gov.in</p>
                </div>
              </div>
            </div>

            {/* Input */}
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Ask about a suspected scam…"
                disabled
                aria-label="Chat input (coming in Day 2)"
                className="flex-1 rounded-lg border border-[var(--input)] bg-[var(--background)] px-4 py-2.5 text-sm placeholder:text-[var(--muted-foreground)] disabled:opacity-50"
              />
              <Button disabled leftIcon={<Send className="h-4 w-4" />} aria-label="Send message">
                Send
              </Button>
            </div>
            <p className="text-center text-xs text-[var(--muted-foreground)]">
              Full chat integration coming in Day 2
            </p>
          </CardContent>
        </Card>

        {/* Right panel */}
        <div className="flex flex-col gap-6">
          {/* Suggested questions */}
          <Card>
            <CardHeader>
              <CardTitle>Suggested Questions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {sampleQuestions.map((q) => (
                <button
                  key={q}
                  disabled
                  className="w-full rounded-lg border border-[var(--border)] px-3 py-2.5 text-left text-sm text-[var(--foreground)] hover:bg-[var(--muted)] transition-colors disabled:opacity-50"
                >
                  {q}
                </button>
              ))}
            </CardContent>
          </Card>

          {/* Knowledge sources */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="h-4 w-4" aria-hidden="true" />
                Knowledge Sources
              </CardTitle>
              <CardDescription>Verified government advisories</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {sources.map(({ name, type, category }) => (
                <div key={name} className="flex items-start justify-between gap-2">
                  <div>
                    <p className="text-sm font-medium">{name}</p>
                    <p className="text-xs text-[var(--muted-foreground)]">{category}</p>
                  </div>
                  <Badge variant="success">{type}</Badge>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}
