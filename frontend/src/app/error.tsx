"use client";

import { useEffect } from "react";
import { AlertCircle, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/Button";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error("Unhandled error:", error);
  }, [error]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-[var(--background)] p-6 text-center">
      <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-red-100 dark:bg-red-950/30 mb-6">
        <AlertCircle className="h-10 w-10 text-red-600 dark:text-red-400" aria-hidden="true" />
      </div>
      <h1 className="text-2xl font-bold">Something went wrong</h1>
      <p className="mt-2 max-w-sm text-[var(--muted-foreground)]">
        {error.message || "An unexpected error occurred. Please try again."}
      </p>
      {error.digest && (
        <p className="mt-2 font-mono text-xs text-[var(--muted-foreground)]">
          Error ID: {error.digest}
        </p>
      )}
      <Button
        className="mt-6"
        onClick={reset}
        leftIcon={<RefreshCw className="h-4 w-4" />}
      >
        Try again
      </Button>
    </div>
  );
}
