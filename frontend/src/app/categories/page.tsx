/** Categories page — beautiful category cards with large backgrounds. */

"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { Film, Tv, Music, BookOpen, Sparkles, Clapperboard } from "lucide-react";
import { fetchCategories } from "@/services/homeService";
import { SkeletonCard } from "@/components/ui/Skeleton";
import type { Category } from "@/types";

const CATEGORY_ICONS: Record<string, any> = {
  Movies: Film,
  "TV Series": Tv,
  Anime: Sparkles,
  Documentary: BookOpen,
  Music: Music,
  Uncategorized: Clapperboard,
};

export default function CategoriesPage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCategories()
      .then(setCategories)
      .catch(() => setCategories([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 py-6">
      <h1 className="text-2xl sm:text-3xl font-bold text-white mb-6">Categories</h1>

      {loading ? (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {Array.from({ length: 8 }).map((_, i) => <SkeletonCard key={i} />)}
        </div>
      ) : categories.length === 0 ? (
        <p className="text-gray-400 text-center py-20">No categories found</p>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {categories.map((cat, i) => {
            const Icon = CATEGORY_ICONS[cat.name] || Clapperboard;
            return (
              <Link key={cat.slug} href={`/browse?category=${cat.slug}`}>
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.05 }}
                  whileHover={{ scale: 1.03 }}
                  className="relative aspect-[4/3] rounded-2xl overflow-hidden glass-card group"
                >
                  <div className="absolute inset-0 bg-gradient-to-br from-neon-purple/20 to-neon-blue/20" />
                  <div className="absolute inset-0 flex flex-col items-center justify-center p-4">
                    <Icon className="w-10 h-10 text-white mb-3 group-hover:scale-110 transition-transform" />
                    <h3 className="text-lg font-bold text-white">{cat.name}</h3>
                    <p className="text-sm text-gray-300 mt-1">{cat.media_count} items</p>
                  </div>
                  <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                </motion.div>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}
