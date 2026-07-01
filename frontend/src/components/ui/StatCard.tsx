import { cn } from "@/lib/utils";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import { Card, CardContent } from "./Card";
import type { StatCardData } from "@/types";

interface StatCardProps extends StatCardData {
  className?: string;
}

export function StatCard({ label, value, change, changeLabel, icon: Icon, trend = "neutral", className }: StatCardProps) {
  const trendColors = {
    up: "text-emerald-600 dark:text-emerald-400",
    down: "text-red-600 dark:text-red-400",
    neutral: "text-[var(--muted-foreground)]",
  };

  const TrendIcon = trend === "up" ? TrendingUp : trend === "down" ? TrendingDown : Minus;

  return (
    <Card className={cn("transition-shadow hover:shadow-md", className)}>
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <p className="text-sm font-medium text-[var(--muted-foreground)]">{label}</p>
          {Icon && (
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[var(--accent)]">
              <Icon className="h-5 w-5 text-[var(--accent-foreground)]" />
            </div>
          )}
        </div>
        <div className="mt-3">
          <p className="text-3xl font-bold tabular-nums">{value}</p>
          {(change !== undefined || changeLabel) && (
            <div className={cn("mt-1 flex items-center gap-1 text-sm", trendColors[trend])}>
              <TrendIcon className="h-4 w-4" aria-hidden="true" />
              {change !== undefined && (
                <span>{change > 0 ? "+" : ""}{change}%</span>
              )}
              {changeLabel && <span className="text-[var(--muted-foreground)]">{changeLabel}</span>}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
