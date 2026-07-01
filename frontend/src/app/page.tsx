import Link from "next/link";
import { Shield, ArrowRight, ScanLine, Network, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card, CardContent } from "@/components/ui/Card";

const features = [
  {
    icon: ScanLine,
    title: "Currency Scanner",
    description: "AI-powered EfficientNet model to detect counterfeit Indian currency notes instantly.",
    href: "/scanner",
    color: "bg-blue-100 dark:bg-blue-950/40 text-blue-700 dark:text-blue-400",
  },
  {
    icon: Network,
    title: "Fraud Network",
    description: "Graph-based fraud intelligence using Neo4j to map and expose fraud networks.",
    href: "/fraud-network",
    color: "bg-purple-100 dark:bg-purple-950/40 text-purple-700 dark:text-purple-400",
  },
  {
    icon: ShieldCheck,
    title: "Scam Shield",
    description: "RAG-powered chatbot grounded in real CERT-In and RBI advisories to combat digital arrest scams.",
    href: "/scam-shield",
    color: "bg-emerald-100 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400",
  },
];

export default function HomePage() {
  return (
    <div className="flex min-h-screen flex-col">
      {/* Hero */}
      <main className="flex flex-1 flex-col items-center justify-center bg-gradient-to-b from-[var(--accent)] to-[var(--background)] px-6 py-24 text-center">
        <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-[var(--primary)] shadow-lg mb-8">
          <Shield className="h-10 w-10 text-white" aria-hidden="true" />
        </div>
        <h1 className="max-w-2xl text-4xl font-bold tracking-tight sm:text-5xl">
          Digital Public Safety Platform
        </h1>
        <p className="mt-4 max-w-xl text-lg text-[var(--muted-foreground)]">
          AI-powered tools to defeat counterfeit currency, fraud networks, and digital arrest scams.
          Built for India&apos;s digital safety.
        </p>
        <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
          <Link href="/dashboard">
            <Button size="lg" rightIcon={<ArrowRight className="h-4 w-4" />}>
              Open Dashboard
            </Button>
          </Link>
          <Link href="/about">
            <Button size="lg" variant="outline">
              Learn More
            </Button>
          </Link>
        </div>

        {/* Feature Cards */}
        <div className="mt-20 grid w-full max-w-4xl grid-cols-1 gap-6 sm:grid-cols-3">
          {features.map(({ icon: Icon, title, description, href, color }) => (
            <Link key={href} href={href} className="group">
              <Card className="h-full transition-shadow hover:shadow-md">
                <CardContent className="p-6 text-left">
                  <div className={`mb-4 flex h-12 w-12 items-center justify-center rounded-xl ${color}`}>
                    <Icon className="h-6 w-6" aria-hidden="true" />
                  </div>
                  <h2 className="font-semibold">{title}</h2>
                  <p className="mt-1 text-sm text-[var(--muted-foreground)]">{description}</p>
                  <p className="mt-3 flex items-center gap-1 text-sm font-medium text-[var(--primary)]">
                    Open <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-1" aria-hidden="true" />
                  </p>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      </main>

      <footer className="border-t border-[var(--border)] py-6 text-center text-sm text-[var(--muted-foreground)]">
        © 2026 ET AI Hackathon — Digital Public Safety Platform
      </footer>
    </div>
  );
}
