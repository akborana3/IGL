/** Reusable skeleton with shimmer effect. */

import { cn } from "@/lib/utils";

interface SkeletonProps {
  className?: string;
}

export function Skeleton({ className }: SkeletonProps) {
  return <div className={cn("skeleton rounded-lg", className)} />;
}

export function SkeletonCard() {
  return (
    <div className="flex flex-col gap-3">
      <Skeleton className="aspect-video w-full rounded-xl" />
      <Skeleton className="h-4 w-3/4" />
      <Skeleton className="h-3 w-1/2" />
    </div>
  );
}

export function SkeletonRow({ count = 5 }: { count?: number }) {
  return (
    <div className="flex gap-4 overflow-hidden px-4">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="min-w-[240px] max-w-[240px]">
          <SkeletonCard />
        </div>
      ))}
    </div>
  );
}
