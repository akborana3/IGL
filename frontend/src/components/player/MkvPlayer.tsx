/** Artplayer-based video player for MKV files.
 *
 * The backend remuxes MKV → fragmented MP4 via FFmpeg pipe.
 * Artplayer plays the fMP4 stream via Media Source Extensions.
 */

"use client";

import { useEffect, useRef } from "react";
import Artplayer from "artplayer";
import { useWatchHistoryStore } from "@/stores/watchHistory";

interface MkvPlayerProps {
  src: string;
  title: string;
  slug: string;
  poster?: string;
  initialPosition?: number;
}

export function MkvPlayer({ src, title, slug, poster, initialPosition }: MkvPlayerProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const artRef = useRef<Artplayer | null>(null);
  const { updateProgress } = useWatchHistoryStore();

  useEffect(() => {
    if (!containerRef.current) return;

    const art = new Artplayer({
      container: containerRef.current,
      url: src,
      title: title,
      poster: poster || "",
      volume: 1,
      autoplay: true,
      pip: true,
      fullscreen: true,
      fullscreenWeb: true,
      playbackRate: true,
      aspectRatio: true,
      setting: true,
      hotkey: true,
      theme: "#a855f7",
      lang: "en",
      type: "mp4", // backend remuxes MKV → fMP4, so tell Artplayer it's MP4
      customType: {
        mp4: (video: HTMLVideoElement, url: string) => {
          // Use native video element — fMP4 is supported by HTML5 video
          video.src = url;
        },
      },
    });

    artRef.current = art;

    // Resume playback from saved position
    if (initialPosition && initialPosition > 0) {
      art.once("ready", () => {
        art.currentTime = initialPosition;
      });
    }

    // Track progress every 5 seconds
    const progressInterval = setInterval(() => {
      if (art.duration > 0) {
        updateProgress({
          slug,
          title,
          thumbnail: poster || null,
          progress: art.currentTime / art.duration,
          position: art.currentTime,
          duration: art.duration,
          lastWatched: Date.now(),
        });
      }
    }, 5000);

    return () => {
      clearInterval(progressInterval);
      art.destroy(false);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [src]);

  return (
    <div className="w-full max-w-5xl mx-auto">
      <div
        ref={containerRef}
        className="rounded-2xl overflow-hidden shadow-premium"
        style={{ aspectRatio: "16 / 9" }}
      />
    </div>
  );
}
