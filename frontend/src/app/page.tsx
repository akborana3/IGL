/** Homepage — hero banner, trending, continue watching, recently added, etc. */
"use client";

"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { HeroBanner } from "@/components/home/HeroBanner";
import { MediaRow } from "@/components/home/MediaRow";
import { ContinueWatching } from "@/components/home/ContinueWatching";
import { SkeletonRow } from "@/components/ui/Skeleton";
import { ScrollReveal } from "@/components/ui/ScrollReveal";
import { fetchHomeData } from "@/services/homeService";
import type { HomeData } from "@/types";
import { APP_NAME } from "@/lib/constants";
import Link from "next/link";

export default function HomePage() {
  const [data, setData] = useState<HomeData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHomeData()
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="mx-auto max-w-7xl px-0 sm:px-6 py-4">
      {/* Hero */}
      {loading ? (
        <div className="w-full h-[60vh] min-h-[400px] skeleton rounded-3xl" />
      ) : error ? (
        <div className="w-full h-[40vh] flex items-center justify-center rounded-3xl glass">
          <p className="text-gray-400">Unable to load content. Please try again later.</p>
        </div>
      ) : (
        <HeroBanner items={data?.hero || []} />
      )}

      {/* Continue Watching (local) */}
      <div className="mt-8">
        <ContinueWatching />
      </div>

      {/* Trending */}
      {loading ? (
        <div className="mb-8">
          <div className="h-6 w-40 skeleton rounded mb-4 mx-4" />
          <SkeletonRow />
        </div>
      ) : (
        <MediaRow title="Trending This Week" items={data?.trending || []} />
      )}

      {/* Recently Added */}
      {loading ? (
        <div className="mb-8">
          <div className="h-6 w-40 skeleton rounded mb-4 mx-4" />
          <SkeletonRow />
        </div>
      ) : (
        <MediaRow title="Recently Added" items={data?.recently_added || []} />
      )}

      {/* Most Popular */}
      {loading ? (
        <div className="mb-8">
          <div className="h-6 w-40 skeleton rounded mb-4 mx-4" />
          <SkeletonRow />
        </div>
      ) : (
        <MediaRow title="Most Popular" items={data?.popular || []} />
      )}

      {/* Top Rated */}
      {loading ? (
        <div className="mb-8">
          <div className="h-6 w-40 skeleton rounded mb-4 mx-4" />
          <SkeletonRow />
        </div>
      ) : (
        <MediaRow title="Top Rated" items={data?.top_rated || []} />
      )}

      {/* Categories */}
      {!loading && data?.categories && data.categories.length > 0 && (
        <ScrollReveal className="mb-8 px-4">
          <h2 className="text-lg sm:text-xl font-bold text-white mb-4">Categories</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
            {data.categories.map((cat) => (
              <Link key={cat.slug} href={`/browse?category=${cat.slug}`}>
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  className="glass-card p-4 rounded-xl text-center"
                >
                  <p className="text-sm font-semibold text-white">{cat.name}</p>
                  <p className="text-xs text-gray-400 mt-1">{cat.media_count} items</p>
                </motion.div>
              </Link>
            ))}
          </div>
        </ScrollReveal>
      )}

      {/* Featured Collections */}
      {data?.featured_collections && data.featured_collections.length > 0 && (
        <MediaRow title="Featured Collections" items={data.featured_collections} />
      )}

      {/* Latest Uploads */}
      {data?.latest_uploads && (
        <MediaRow title="Latest Uploads" items={data.latest_uploads} />
      )}
    </div>
  );
}