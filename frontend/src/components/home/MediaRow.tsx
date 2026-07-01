/** Horizontal scrolling row of MediaCards with scroll reveal animation. */
"use client";

"use client";

import { motion } from "framer-motion";
import { useRef } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { MediaCard } from "@/components/media/MediaCard";
import { ScrollReveal } from "@/components/ui/ScrollReveal";
import type { Media } from "@/types";

interface MediaRowProps {
  title: string;
  items: Media[];
  progressMap?: Record<string, number>;
}

export function MediaRow({ title, items, progressMap }: MediaRowProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  const scroll = (dir: "left" | "right") => {
    if (!scrollRef.current) return;
    const amount = scrollRef.current.clientWidth * 0.8;
    scrollRef.current.scrollBy({ left: dir === "left" ? -amount : amount, behavior: "smooth" });
  };

  if (!items.length) return null;

  return (
    <ScrollReveal className="mb-8">
      <div className="flex items-center justify-between mb-4 px-4">
        <h2 className="text-lg sm:text-xl font-bold text-white">{title}</h2>
        <div className="hidden sm:flex gap-2">
          <button
            onClick={() => scroll("left")}
            className="p-1.5 rounded-full glass hover:bg-white/10 transition-colors"
            aria-label="Scroll left"
          >
            <ChevronLeft size={18} className="text-white" />
          </button>
          <button
            onClick={() => scroll("right")}
            className="p-1.5 rounded-full glass hover:bg-white/10 transition-colors"
            aria-label="Scroll right"
          >
            <ChevronRight size={18} className="text-white" />
          </button>
        </div>
      </div>

      <div
        ref={scrollRef}
        className="flex gap-4 overflow-x-auto scrollbar-hide px-4 pb-2 snap-x"
      >
        {items.map((media, i) => (
          <motion.div
            key={media.id}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.05, duration: 0.3 }}
            className="min-w-[240px] max-w-[240px] snap-start"
          >
            <MediaCard
              media={media}
              progress={progressMap?.[media.slug]}
            />
          </motion.div>
        ))}
      </div>
    </ScrollReveal>
  );
}