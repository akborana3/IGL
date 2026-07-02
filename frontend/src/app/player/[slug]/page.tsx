/** Video player page — conditional Vidstack (MP4) or Artplayer (MKV). */

"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { VideoPlayer } from "@/components/player/VideoPlayer";
import { MkvPlayer } from "@/components/player/MkvPlayer";
import { fetchMediaDetail } from "@/services/mediaService";
import { getStreamUrl, getStreamUrlWithFormat } from "@/services/streamService";
import { useWatchHistoryStore } from "@/stores/watchHistory";
import { Spinner } from "@/components/ui/Spinner";
import type { MediaDetail } from "@/types";

export default function PlayerPage() {
  const { slug } = useParams<{ slug: string }>();
  const [media, setMedia] = useState<MediaDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const { getProgress } = useWatchHistoryStore();

  useEffect(() => {
    if (!slug) return;
    fetchMediaDetail(slug)
      .then(setMedia)
      .catch(() => setMedia(null))
      .finally(() => setLoading(false));
  }, [slug]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Spinner size={40} />
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

  const savedProgress = getProgress(media.slug);
  const initialPosition = savedProgress?.position || 0;

  // Detect MKV — use Artplayer, otherwise Vidstack
  const { url: streamUrl, isMkv } = getStreamUrlWithFormat(
    media.telegram_message_id,
    media.mime_type
  );

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 py-6">
      {/* Back button */}
      <Link href={`/media/${media.slug}`} className="inline-flex items-center gap-2 text-gray-400 hover:text-white mb-4 transition-colors">
        <ArrowLeft size={18} /> Back to Details
      </Link>

      {/* Conditional player */}
      {isMkv ? (
        <MkvPlayer
          src={streamUrl}
          title={media.title}
          slug={media.slug}
          poster={media.thumbnail || undefined}
          initialPosition={initialPosition}
        />
      ) : (
        <VideoPlayer
          src={getStreamUrl(media.telegram_message_id)}
          title={media.title}
          slug={media.slug}
          poster={media.thumbnail || undefined}
          initialPosition={initialPosition}
        />
      )}

      {/* Title below player */}
      <div className="mt-6">
        <h1 className="text-xl sm:text-2xl font-bold text-white">{media.title}</h1>
        <div className="flex flex-wrap gap-3 mt-2 text-sm text-gray-400">
          <span>{media.category}</span>
          {media.duration > 0 && <span>• {Math.floor(media.duration / 60)} min</span>}
          {isMkv && <span className="text-neon-purple">• MKV → fMP4 remux</span>}
          {savedProgress && (
            <span className="text-neon-purple">• Resumed from {Math.floor(savedProgress.position / 60)} min</span>
          )}
        </div>
      </div>
    </div>
  );
}
