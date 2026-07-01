/** Premium loading spinner. */

import { cn } from "@/lib/utils";

interface SpinnerProps {
  className?: string;
  size?: number;
}

export function Spinner({ className, size = 24 }: SpinnerProps) {
  return (
    <div
      className={cn("inline-block animate-spin rounded-full border-2 border-neon-purple/30 border-t-neon-purple", className)}
      style={{ width: size, height: size }}
      role="status"
      aria-label="Loading"
    />
  );
}
