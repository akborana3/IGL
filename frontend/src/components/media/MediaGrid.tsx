/** Responsive grid layout for browse/search pages. */

import { MediaCard } from "./MediaCard";
import type { Media } from "@/types";

interface MediaGridProps {
  items: Media[];
  className?: string;
}

export function MediaGrid({ items, className }: MediaGridProps) {
  return (
    <div className={className}>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        {items.map((media) => (
          <MediaCard key={media.id} media={media} />
        ))}
      </div>
    </div>
  );
}
