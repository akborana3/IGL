/** Media detail page — cinematic header, glass info panel, related media. */

"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { motion } from "framer-motion";
import Link from "next/link";
import { Play, Download, Share2, Heart, Eye, Clock, Calendar, Tag, HardDrive } from "lucide-react";
import { fetchMediaDetail } from "@/services/mediaService";
import { getDownloadUrl } from "@/services/streamService";
import { useFavoritesStore } from "@/stores/favorites";
import { MagneticButton } from "@/components/ui/MagneticButton";
import { MediaRow } from "@/components/home/MediaRow";
import { SkeletonCard } from "@/components/ui/Skeleton";
import { formatDuration, formatFileSize, formatDate, formatCount, getResolutionLabel, getThumbnailUrl } from "@/lib/utils";
import type { MediaDetail } from "@/types";

export default function MediaDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const [media, setMedia] = useState<MediaDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [shared, setShared] = useState(false);
  const { isFavorite, addFavorite, removeFavorite } = useFavoritesStore();

  useEffect(() => {
    if (!slug) return;
    fetchMediaDetail(slug)
      .then(setMedia)
      .catch(() => setMedia(null))
      .finally(() => setLoading(false));
  }, [slug]);

  const handleShare = async () => {
    if (navigator.share) {
      try { await navigator.share({ title: media?.title, url: window.location.href }); } catch {}
    } else {
      await navigator.clipboard.writeText(window.location.href);
      setShared(true);
      setTimeout(() => setShared(false), 2000);
    }
  };

  const handleFavorite = () => {
    if (!media) return;
    if (isFavorite(media.slug)) {
      removeFavorite(media.slug);
    } else {
      addFavorite({ slug: media.slug, title: media.title, thumbnail: media.thumbnail, addedAt: Date.now() });
    }
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-5xl px-4 sm:px-6 py-6">
        <SkeletonCard />
      </div>
    );
  }

  if (!media) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <p className="text-gray-400 text-lg">Media not found</p>
        <Link href="/browse" className="text-neon-purple mt-4 hover:underline">Back to Browse</Link>
      </div>
    );
  }

  const fav = isFavorite(media.slug);

  return (
    <div className="mx-auto max-w-5xl px-4 sm:px-6 py-6">
      {/* Cinematic header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative w-full h-[40vh] min-h-[300px] rounded-3xl overflow-hidden mb-6"
      >
        {getThumbnailUrl(media.thumbnail, media.telegram_message_id) ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={getThumbnailUrl(media.thumbnail, media.telegram_message_id) || ""} alt={media.title} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-[#1a0b2e] to-[#0f172a]" />
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-[#0a0a0f] via-[#0a0a0f]/50 to-transparent" />
      </motion.div>

      {/* Info panel */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="glass-strong rounded-2xl p-6 sm:p-8 -mt-20 relative z-10"
      >
        <h1 className="text-2xl sm:text-4xl font-bold text-white mb-3">{media.title}</h1>

        {/* Meta row */}
        <div className="flex flex-wrap items-center gap-4 text-sm text-gray-400 mb-4">
          {media.duration > 0 && (
            <span className="flex items-center gap-1"><Clock size={14} /> {formatDuration(media.duration)}</span>
          )}
          <span className="flex items-center gap-1"><Calendar size={14} /> {formatDate(media.upload_date)}</span>
          <span className="flex items-center gap-1"><Eye size={14} /> {formatCount(media.views)} views</span>
          <span className="flex items-center gap-1"><Download size={14} /> {formatCount(media.downloads)} downloads</span>
          {media.width > 0 && <span className="px-2 py-0.5 rounded bg-white/10">{getResolutionLabel(media.width, media.height)}</span>}
          {media.file_size > 0 && (
            <span className="flex items-center gap-1"><HardDrive size={14} /> {formatFileSize(media.file_size)}</span>
          )}
        </div>

        {/* Description */}
        {media.description && (
          <p className="text-gray-300 text-sm sm:text-base mb-6 leading-relaxed">{media.description}</p>
        )}

        {/* Tags */}
        {media.tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-6">
            {media.tags.map((tag) => (
              <span key={tag} className="px-3 py-1 rounded-full text-xs bg-white/5 text-gray-400 border border-white/10">
                {tag}
              </span>
            ))}
          </div>
        )}

        {/* Action buttons */}
        <div className="flex flex-wrap gap-3">
          <Link href={`/player/${media.slug}`}>
            <MagneticButton className="flex items-center gap-2">
              <Play size={18} fill="white" /> Watch Now
            </MagneticButton>
          </Link>
          <a href={getDownloadUrl(media.telegram_message_id)} target="_blank" rel="noopener noreferrer">
            <button className="px-6 py-3 rounded-xl glass-strong text-white font-medium hover:bg-white/10 transition-colors flex items-center gap-2">
              <Download size={18} /> Download
            </button>
          </a>
          <button
            onClick={handleFavorite}
            className="px-6 py-3 rounded-xl glass-strong text-white font-medium hover:bg-white/10 transition-colors flex items-center gap-2"
          >
            <Heart size={18} className={fav ? "text-neon-pink" : ""} fill={fav ? "currentColor" : "none"} />
            {fav ? "Favorited" : "Favorite"}
          </button>
          <button
            onClick={handleShare}
            className="px-6 py-3 rounded-xl glass-strong text-white font-medium hover:bg-white/10 transition-colors flex items-center gap-2"
          >
            <Share2 size={18} /> {shared ? "Copied!" : "Share"}
          </button>
        </div>
      </motion.div>

      {/* Related media */}
      {media.related && media.related.length > 0 && (
        <div className="mt-8">
          <MediaRow title="Related Media" items={media.related} />
        </div>
      )}
    </div>
  );
}
