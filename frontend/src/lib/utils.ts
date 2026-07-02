/** Utility functions for the frontend. */

import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/** Merge Tailwind classes intelligently. */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/** Format seconds into H:MM:SS or M:SS. */
export function formatDuration(seconds: number): string {
  if (!seconds || seconds <= 0) return "0:00";
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);
  if (hours > 0) return `${hours}:${minutes.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  return `${minutes}:${secs.toString().padStart(2, "0")}`;
}

/** Format bytes into human-readable string. */
export function formatFileSize(bytes: number): string {
  if (!bytes || bytes <= 0) return "0 B";
  const units = ["B", "KB", "MB", "GB", "TB"];
  let idx = 0;
  let size = bytes;
  while (size >= 1024 && idx < units.length - 1) {
    size /= 1024;
    idx++;
  }
  return idx === 0 ? `${size} ${units[idx]}` : `${size.toFixed(1)} ${units[idx]}`;
}

/** Format a date string into a readable format. */
export function formatDate(date: string | Date): string {
  const d = typeof date === "string" ? new Date(date) : date;
  return d.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

/** Format view/download counts with K/M suffixes. */
export function formatCount(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
  return `${n}`;
}

/** Debounce a function call. */
export function debounce<T extends (...args: any[]) => void>(fn: T, delay: number): (...args: Parameters<T>) => void {
  let timer: ReturnType<typeof setTimeout>;
  return (...args: Parameters<T>) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

/** Get the thumbnail URL for a media item.
 * Uses the stored thumbnail URL if available, otherwise falls back
 * to the backend /api/thumbnail/{message_id} endpoint.
 */
export function getThumbnailUrl(thumbnail: string | null, messageId: number): string | null {
  if (thumbnail) return thumbnail;
  // Fall back to backend thumbnail endpoint
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:7860";
  return `${apiUrl}/api/thumbnail/${messageId}`;
}

/** Get a resolution label from width/height. */
export function getResolutionLabel(width: number, height: number): string {
  if (height >= 2160) return "4K";
  if (height >= 1080) return "1080p";
  if (height >= 720) return "720p";
  if (height >= 480) return "480p";
  return height > 0 ? `${height}p` : "HD";
}
