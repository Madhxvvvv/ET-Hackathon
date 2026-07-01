import { PageSpinner } from "@/components/ui/Spinner";

export default function Loading() {
  return (
    <div className="flex h-screen items-center justify-center">
      <PageSpinner />
    </div>
  );
}
