/** Large cinematic auto-rotating hero banner with glass info panel. */

"use client";

import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import { Play, Info } from "lucide-react";
import { useEffect, useState } from "react";
import type { Media } from "@/types";
import { formatDuration, getThumbnailUrl } from "@/lib/utils";
import { MagneticButton } from "@/components/ui/MagneticButton";

interface HeroBannerProps {
  items: Media[];
}

export function HeroBanner({ items }: HeroBannerProps) {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (items.length <= 1) return;
    const timer = setInterval(() => {
      setIndex((prev) => (prev + 1) % items.length);
    }, 8000);
    return () => clearInterval(timer);
  }, [items.length]);

  if (!items.length) return null;

  const current = items[index];

  return (
    <div className="relative w-full h-[60vh] min-h-[400px] max-h-[700px] overflow-hidden rounded-3xl">
      <AnimatePresence mode="wait">
        <motion.div
          key={current.slug}
          initial={{ opacity: 0, scale: 1.05 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 1.02 }}
          transition={{ duration: 1, ease: "easeInOut" }}
          className="absolute inset-0"
        >
          {getThumbnailUrl(current.thumbnail, current.telegram_message_id) ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={getThumbnailUrl(current.thumbnail, current.telegram_message_id) || ""}
              alt={current.title}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-full h-full bg-gradient-to-br from-[#1a0b2e] via-[#0f172a] to-[#1e1b4b]" />
          )}
        </motion.div>
      </AnimatePresence>

      {/* Gradient overlays */}
      <div className="absolute inset-0 bg-gradient-to-t from-[#0a0a0f] via-[#0a0a0f]/40 to-transparent" />
      <div className="absolute inset-0 bg-gradient-to-r from-[#0a0a0f]/80 via-transparent to-transparent" />

      {/* Info panel */}
      <AnimatePresence mode="wait">
        <motion.div
          key={current.slug}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="absolute bottom-0 left-0 right-0 p-6 sm:p-10"
        >
          <div className="max-w-2xl">
            {current.featured && (
              <span className="inline-block px-3 py-1 rounded-full text-xs font-medium bg-neon-purple/30 backdrop-blur-sm text-neon-purple mb-3">
                Featured
              </span>
            )}
            <h1 className="text-3xl sm:text-5xl font-bold text-white mb-3 neon-text">
              {current.title}
            </h1>
            <p className="text-gray-300 text-sm sm:text-base mb-4 line-clamp-2 max-w-xl">
              {current.description || current.caption}
            </p>
            <div className="flex items-center gap-4 mb-5 text-sm text-gray-400">
              {current.duration > 0 && <span>{formatDuration(current.duration)}</span>}
              <span>{current.category}</span>
              {current.tags.length > 0 && <span>{current.tags[0]}</span>}
            </div>
            <div className="flex gap-3">
              <Link href={`/player/${current.slug}`}>
                <MagneticButton className="flex items-center gap-2">
                  <Play size={18} fill="white" /> Watch Now
                </MagneticButton>
              </Link>
              <Link href={`/media/${current.slug}`}>
                <button className="px-6 py-3 rounded-xl glass-strong text-white font-medium hover:bg-white/10 transition-colors flex items-center gap-2">
                  <Info size={18} /> More Info
                </button>
              </Link>
            </div>
          </div>
        </motion.div>
      </AnimatePresence>

      {/* Dots indicator */}
      {items.length > 1 && (
        <div className="absolute bottom-4 right-6 flex gap-2">
          {items.map((_, i) => (
            <button
              key={i}
              onClick={() => setIndex(i)}
              className={`h-1.5 rounded-full transition-all ${
                i === index ? "w-8 bg-neon-purple" : "w-1.5 bg-white/30"
              }`}
              aria-label={`Slide ${i + 1}`}
            />
          ))}
        </div>
      )}
    </div>
  );
}
