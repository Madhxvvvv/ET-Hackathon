import Link from "next/link";
import { Shield, Home } from "lucide-react";
import { Button } from "@/components/ui/Button";

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-[var(--background)] p-6 text-center">
      <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-[var(--accent)] mb-6">
        <Shield className="h-10 w-10 text-[var(--accent-foreground)]" aria-hidden="true" />
      </div>
      <h1 className="text-6xl font-bold text-[var(--primary)]">404</h1>
      <h2 className="mt-2 text-2xl font-semibold">Page Not Found</h2>
      <p className="mt-3 max-w-sm text-[var(--muted-foreground)]">
        The page you are looking for does not exist or has been moved.
      </p>
      <div className="mt-8 flex gap-3">
        <Link href="/dashboard">
          <Button leftIcon={<Home className="h-4 w-4" />}>
            Go to Dashboard
          </Button>
        </Link>
        <Link href="/">
          <Button variant="outline">
            Home
          </Button>
        </Link>
      </div>
    </div>
  );
}
