/** Reusable glassmorphism card component. */

"use client";

import { motion, HTMLMotionProps } from "framer-motion";
import { cn } from "@/lib/utils";
import { forwardRef } from "react";

interface GlassCardProps extends HTMLMotionProps<"div"> {
  hover?: boolean;
  glow?: boolean;
}

export const GlassCard = forwardRef<HTMLDivElement, GlassCardProps>(
  ({ className, hover = true, glow = false, children, ...props }, ref) => {
    return (
      <motion.div
        ref={ref}
        className={cn(
          "glass-card rounded-2xl",
          hover && "hover:scale-[1.02] hover:shadow-premium cursor-pointer",
          glow && "animate-glow-pulse",
          className
        )}
        {...props}
      >
        {children}
      </motion.div>
    );
  }
);

GlassCard.displayName = "GlassCard";
