/** Continue watching row from local storage with progress indicators. */

"use client";

import { MediaRow } from "./MediaRow";
import { useWatchHistoryStore } from "@/stores/watchHistory";
import { SkeletonRow } from "@/components/ui/Skeleton";

export function ContinueWatching() {
  const { history } = useWatchHistoryStore();

  if (!history.length) return null;

  // Convert history items to a format MediaRow can use
  // We need to fetch media details, but for simplicity we show what we have
  const progressMap: Record<string, number> = {};
  history.forEach((item) => {
    progressMap[item.slug] = item.progress;
  });

  // Map history to a minimal media-like object
  const items = history.map((h) => ({
    id: h.slug,
    telegram_message_id: 0,
    title: h.title,
    slug: h.slug,
    category: "",
    tags: [],
    duration: h.duration,
    width: 0,
    height: 0,
    file_size: 0,
    mime_type: "",
    thumbnail: h.thumbnail,
    upload_date: "",
    views: 0,
    downloads: 0,
    featured: false,
    description: "",
    caption: "",
  }));

  return <MediaRow title="Continue Watching" items={items} progressMap={progressMap} />;
}
