import type { Metadata } from "next";
import { ScanLine, Upload, Camera, FileImage } from "lucide-react";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card";
import { Alert } from "@/components/ui/Alert";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";

export const metadata: Metadata = { title: "Currency Scanner" };

export default function ScannerPage() {
  return (
    <DashboardLayout>
      <PageHeader
        title="Currency Scanner"
        description="Upload or capture an Indian currency note to detect counterfeits using AI."
        breadcrumbs={[{ label: "Dashboard", href: "/dashboard" }, { label: "Currency Scanner" }]}
      />

      <Alert variant="warning" title="Module Under Development" className="mb-6">
        The EfficientNet model is being trained. Upload functionality will be enabled in Day 2.
      </Alert>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Upload area */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Upload Note Image</CardTitle>
            <CardDescription>Supports JPG, PNG, BMP · Max 10 MB</CardDescription>
          </CardHeader>
          <CardContent>
            <div
              className="flex min-h-64 flex-col items-center justify-center rounded-xl border-2 border-dashed border-[var(--border)] bg-[var(--muted)]/40 p-10 text-center transition-colors hover:border-[var(--primary)] hover:bg-[var(--accent)]/30"
              role="region"
              aria-label="File upload area"
            >
              <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-[var(--accent)]">
                <Upload className="h-8 w-8 text-[var(--accent-foreground)]" aria-hidden="true" />
              </div>
              <p className="text-base font-medium">Drag & drop or click to upload</p>
              <p className="mt-1 text-sm text-[var(--muted-foreground)]">JPG, PNG, BMP up to 10 MB</p>
              <div className="mt-6 flex gap-3">
                <Button variant="default" leftIcon={<FileImage className="h-4 w-4" />} disabled>
                  Choose File
                </Button>
                <Button variant="outline" leftIcon={<Camera className="h-4 w-4" />} disabled>
                  Use Camera
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Result panel */}
        <Card>
          <CardHeader>
            <CardTitle>Analysis Result</CardTitle>
            <CardDescription>AI classification output</CardDescription>
          </CardHeader>
          <CardContent>
            <EmptyState
              title="No image uploaded"
              description="Upload a note image to see the classification result."
              icon={<ScanLine className="h-8 w-8 text-[var(--muted-foreground)]" />}
            />
          </CardContent>
        </Card>
      </div>

      {/* How it works */}
      <Card className="mt-6">
        <CardHeader>
          <CardTitle>How It Works</CardTitle>
        </CardHeader>
        <CardContent>
          <ol className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            {[
              { step: "1", title: "Upload Image", desc: "Take a clear photo of the currency note." },
              { step: "2", title: "AI Analysis", desc: "EfficientNet-B0 analyses security features." },
              { step: "3", title: "Get Result", desc: "Receive genuine/counterfeit verdict with confidence score." },
            ].map(({ step, title, desc }) => (
              <li key={step} className="flex gap-4">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-[var(--accent)] text-sm font-bold text-[var(--accent-foreground)]">
                  {step}
                </div>
                <div>
                  <p className="font-medium">{title}</p>
                  <p className="text-sm text-[var(--muted-foreground)]">{desc}</p>
                </div>
              </li>
            ))}
          </ol>
        </CardContent>
      </Card>
    </DashboardLayout>
  );
}
