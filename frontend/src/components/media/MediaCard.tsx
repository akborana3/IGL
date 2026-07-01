/** Media card with thumbnail, glass overlay, hover animations, badges, and actions. */

"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { Play, Download, Share2, Heart, Eye } from "lucide-react";
import type { Media } from "@/types";
import { formatDuration, formatCount, getResolutionLabel, cn } from "@/lib/utils";
import { MediaCard3DTilt } from "./MediaCard3DTilt";
import { useFavoritesStore } from "@/stores/favorites";
import { useState } from "react";

interface MediaCardProps {
  media: Media;
  progress?: number; // 0-1 for continue watching
  className?: string;
}

export function MediaCard({ media, progress, className }: MediaCardProps) {
  const { isFavorite, addFavorite, removeFavorite } = useFavoritesStore();
  const fav = isFavorite(media.slug);
  const [shared, setShared] = useState(false);

  const handleShare = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (navigator.share) {
      try {
        await navigator.share({ title: media.title, url: `/media/${media.slug}` });
      } catch {}
    } else {
      await navigator.clipboard.writeText(`${window.location.origin}/media/${media.slug}`);
      setShared(true);
      setTimeout(() => setShared(false), 2000);
    }
  };

  const handleFavorite = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (fav) {
      removeFavorite(media.slug);
    } else {
      addFavorite({
        slug: media.slug,
        title: media.title,
        thumbnail: media.thumbnail,
        addedAt: Date.now(),
      });
    }
  };

  return (
    <MediaCard3DTilt className="group relative">
      <Link href={`/media/${media.slug}`} className="block">
        <div className={cn("relative aspect-video rounded-xl overflow-hidden glass-card", className)}>
          {/* Thumbnail / placeholder */}
          {media.thumbnail ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={media.thumbnail}
              alt={media.title}
              loading="lazy"
              className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
            />
          ) : (
            <div className="w-full h-full bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center">
              <Play className="w-12 h-12 text-gray-600" />
            </div>
          )}

          {/* Gradient overlay */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-60 group-hover:opacity-90 transition-opacity" />

          {/* Top badges */}
          <div className="absolute top-2 left-2 flex gap-1.5">
            <span className="px-2 py-0.5 rounded-md text-[10px] font-medium bg-black/60 backdrop-blur-sm text-white">
              {getResolutionLabel(media.width, media.height)}
            </span>
            {media.featured && (
              <span className="px-2 py-0.5 rounded-md text-[10px] font-medium bg-neon-purple/80 backdrop-blur-sm text-white">
                Featured
              </span>
            )}
          </div>

          {/* Duration badge */}
          {media.duration > 0 && (
            <span className="absolute bottom-2 right-2 px-1.5 py-0.5 rounded text-[10px] font-medium bg-black/70 backdrop-blur-sm text-white">
              {formatDuration(media.duration)}
            </span>
          )}

          {/* Hover actions */}
          <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
            <div className="flex gap-2">
              <button className="p-2.5 rounded-full glass-strong hover:bg-neon-purple/30 transition-colors">
                <Play className="w-5 h-5 text-white" fill="white" />
              </button>
            </div>
          </div>

          {/* Bottom info */}
          <div className="absolute bottom-0 left-0 right-0 p-3">
            <h3 className="text-sm font-semibold text-white truncate">{media.title}</h3>
            <div className="flex items-center gap-3 mt-1 text-[10px] text-gray-300">
              <span className="flex items-center gap-1">
                <Eye size={10} /> {formatCount(media.views)}
              </span>
              <span className="flex items-center gap-1">
                <Download size={10} /> {formatCount(media.downloads)}
              </span>
              <span className="px-1.5 py-0.5 rounded bg-white/10">{media.category}</span>
            </div>
          </div>

          {/* Progress bar for continue watching */}
          {progress !== undefined && progress > 0 && (
            <div className="absolute bottom-0 left-0 right-0 h-1 bg-white/20">
              <div className="h-full bg-neon-purple" style={{ width: `${progress * 100}%` }} />
            </div>
          )}

          {/* Action buttons */}
          <div className="absolute top-2 right-2 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <button
              onClick={handleFavorite}
              className="p-1.5 rounded-full glass-strong hover:bg-neon-pink/30 transition-colors"
              aria-label="Toggle favorite"
            >
              <Heart size={14} className={fav ? "text-neon-pink" : "text-white"} fill={fav ? "currentColor" : "none"} />
            </button>
            <button
              onClick={handleShare}
              className="p-1.5 rounded-full glass-strong hover:bg-neon-blue/30 transition-colors"
              aria-label="Share"
            >
              <Share2 size={14} className="text-white" />
            </button>
          </div>
        </div>
      </Link>
    </MediaCard3DTilt>
  );
}
