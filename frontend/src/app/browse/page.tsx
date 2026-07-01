/** Browse page — infinite scroll, grid layout, category filters, sorting. */

"use client";

import { useEffect, useState, useCallback } from "react";
import { useSearchParams } from "next/navigation";
import { MediaGrid } from "@/components/media/MediaGrid";
import { MediaSkeleton } from "@/components/media/MediaSkeleton";
import { Spinner } from "@/components/ui/Spinner";
import { searchMedia } from "@/services/searchService";
import { SORT_OPTIONS } from "@/lib/constants";
import type { Media, PaginationInfo } from "@/types";

export default function BrowsePage() {
  const searchParams = useSearchParams();
  const [items, setItems] = useState<Media[]>([]);
  const [pagination, setPagination] = useState<PaginationInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [category, setCategory] = useState(searchParams.get("category") || "");
  const [sort, setSort] = useState("newest");
  const [page, setPage] = useState(1);

  const fetchPage = useCallback(async (p: number, reset: boolean = false) => {
    if (reset) {
      setLoading(true);
    } else {
      setLoadingMore(true);
    }
    try {
      const result = await searchMedia({
        page: p,
        limit: 20,
        category: category || undefined,
        sort,
      });
      setItems(prev => reset ? result.items : [...prev, ...result.items]);
      setPagination(result.pagination);
      setPage(p);
    } catch (e) {
      console.error("Browse error:", e);
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  }, [category, sort]);

  useEffect(() => {
    fetchPage(1, true);
  }, [fetchPage]);

  // Infinite scroll
  useEffect(() => {
    const handler = () => {
      if (loading || loadingMore || !pagination?.has_next) return;
      const scrolled = window.innerHeight + window.scrollY;
      const threshold = document.body.offsetHeight - 500;
      if (scrolled >= threshold) {
        fetchPage(page + 1);
      }
    };
    window.addEventListener("scroll", handler, { passive: true });
    return () => window.removeEventListener("scroll", handler);
  }, [loading, loadingMore, pagination, page, fetchPage]);

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 py-6">
      <h1 className="text-2xl sm:text-3xl font-bold text-white mb-6">Browse</h1>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        <select
          value={category}
          onChange={(e) => { setCategory(e.target.value); }}
          className="px-4 py-2 rounded-xl glass text-sm text-white outline-none cursor-pointer"
        >
          <option value="">All Categories</option>
          <option value="Movies">Movies</option>
          <option value="TV Series">TV Series</option>
          <option value="Anime">Anime</option>
          <option value="Documentary">Documentary</option>
          <option value="Music">Music</option>
        </select>

        <select
          value={sort}
          onChange={(e) => setSort(e.target.value)}
          className="px-4 py-2 rounded-xl glass text-sm text-white outline-none cursor-pointer"
        >
          {SORT_OPTIONS.map(opt => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>
      </div>

      {/* Grid */}
      {loading ? (
        <MediaSkeleton count={20} />
      ) : items.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20">
          <p className="text-gray-400 text-lg">No media found</p>
        </div>
      ) : (
        <>
          <MediaGrid items={items} />
          {loadingMore && (
            <div className="flex justify-center mt-8">
              <Spinner size={32} />
            </div>
          )}
          {pagination && !pagination.has_next && items.length > 0 && (
            <p className="text-center text-gray-500 text-sm mt-8">You've reached the end</p>
          )}
        </>
      )}
    </div>
  );
}
