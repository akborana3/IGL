/** Vidstack video player with premium features. */

"use client";

import { MediaPlayer, MediaProvider } from "@vidstack/react";
import {
  defaultLayoutIcons,
  defaultMediaControls,
  defaultMediaPlayerPlugins,
} from "@vidstack/react/player";
import "@vidstack/react/player/styles/default/theme.css";
import "@vidstack/react/player/styles/default/layouts/video.css";
import { useEffect, useRef } from "react";
import { useWatchHistoryStore } from "@/stores/watchHistory";
import { usePlayerStore } from "@/stores/player";

interface VideoPlayerProps {
  src: string;
  title: string;
  slug: string;
  poster?: string;
  initialPosition?: number;
}

export function VideoPlayer({ src, title, slug, poster, initialPosition }: VideoPlayerProps) {
  const playerRef = useRef<any>(null);
  const { updateProgress } = useWatchHistoryStore();
  const { volume, muted, playbackSpeed, theaterMode } = usePlayerStore();

  // Resume playback from saved position
  useEffect(() => {
    if (!playerRef.current || !initialPosition) return;
    const player = playerRef.current;
    const onLoaded = () => {
      player.currentTime = initialPosition;
    };
    player.addEventListener("can-play", onLoaded, { once: true });
    return () => player.removeEventListener("can-play", onLoaded);
  }, [initialPosition]);

  // Track progress
  useEffect(() => {
    if (!playerRef.current) return;
    const player = playerRef.current;
    const onTimeUpdate = () => {
      const current = player.currentTime;
      const duration = player.duration;
      if (duration > 0) {
        updateProgress({
          slug,
          title,
          thumbnail: poster || null,
          progress: current / duration,
          position: current,
          duration,
          lastWatched: Date.now(),
        });
      }
    };
    const interval = setInterval(onTimeUpdate, 5000);
    return () => clearInterval(interval);
  }, [slug, title, poster, updateProgress]);

  // Keyboard shortcuts
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (!playerRef.current) return;
      const player = playerRef.current;
      switch (e.key) {
        case " ":
        case "k":
          e.preventDefault();
          if (player.paused) player.play(); else player.pause();
          break;
        case "ArrowLeft":
          player.currentTime -= 10;
          break;
        case "ArrowRight":
          player.currentTime += 10;
          break;
        case "f":
          if (player.isFullscreen) player.exitFullscreen(); else player.enterFullscreen();
          break;
        case "m":
          player.muted = !player.muted;
          break;
        case "ArrowUp":
          player.volume = Math.min(1, player.volume + 0.1);
          break;
        case "ArrowDown":
          player.volume = Math.max(0, player.volume - 0.1);
          break;
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  return (
    <div className={`w-full ${theaterMode ? "max-w-none" : "max-w-5xl"} mx-auto`}>
      <MediaPlayer
        ref={playerRef}
        src={src}
        title={title}
        poster={poster}
        streamType="video"
        load="visible"
        playsInline
        autoPlay
        className="rounded-2xl overflow-hidden shadow-premium"
      >
        <MediaProvider />
        {defaultMediaControls({
          plugins: defaultMediaPlayerPlugins,
          icons: defaultLayoutIcons,
        })}
      </MediaPlayer>
    </div>
  );
}
