/** Search page — instant debounced search, highlight, filters, sort. */

"use client";

import { useEffect, useState, useCallback } from "react";
import { Search as SearchIcon, Filter } from "lucide-react";
import { MediaGrid } from "@/components/media/MediaGrid";
import { MediaSkeleton } from "@/components/media/MediaSkeleton";
import { useDebounce } from "@/hooks/useDebounce";
import { searchMedia } from "@/services/searchService";
import { SORT_OPTIONS } from "@/lib/constants";
import type { Media } from "@/types";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const debouncedQuery = useDebounce(query, 300);
  const [category, setCategory] = useState("");
  const [year, setYear] = useState("");
  const [sort, setSort] = useState("newest");
  const [items, setItems] = useState<Media[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [showFilters, setShowFilters] = useState(false);

  const doSearch = useCallback(async () => {
    if (!debouncedQuery && !category && !year) {
      setItems([]);
      setHasSearched(false);
      return;
    }
    setLoading(true);
    setHasSearched(true);
    try {
      const result = await searchMedia({
        q: debouncedQuery,
        category: category || undefined,
        year: year ? parseInt(year) : undefined,
        sort,
        limit: 40,
      });
      setItems(result.items);
    } catch (e) {
      console.error("Search error:", e);
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, [debouncedQuery, category, year, sort]);

  useEffect(() => {
    doSearch();
  }, [doSearch]);

  const highlightMatch = (text: string, match: string) => {
    if (!match) return text;
    const parts = text.split(new RegExp(`(${match})`, "gi"));
    return parts.map((part, i) =>
      part.toLowerCase() === match.toLowerCase() ? (
        <mark key={i} className="bg-neon-purple/30 text-white rounded px-0.5">{part}</mark>
      ) : part
    );
  };

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 py-6">
      {/* Search bar */}
      <div className="relative mb-6">
        <SearchIcon className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" size={20} />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for movies, series, anime..."
          className="w-full pl-12 pr-12 py-4 rounded-2xl glass-strong text-white placeholder-gray-500 outline-none focus:border-neon-purple transition-colors"
          autoFocus
        />
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
          aria-label="Toggle filters"
        >
          <Filter size={20} />
        </button>
      </div>

      {/* Filters */}
      {showFilters && (
        <div className="flex flex-wrap gap-3 mb-6 animate-fade-in">
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="px-4 py-2 rounded-xl glass text-sm text-white outline-none"
          >
            <option value="">All Categories</option>
            <option value="Movies">Movies</option>
            <option value="TV Series">TV Series</option>
            <option value="Anime">Anime</option>
            <option value="Documentary">Documentary</option>
            <option value="Music">Music</option>
          </select>

          <input
            type="number"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            placeholder="Year"
            className="w-24 px-4 py-2 rounded-xl glass text-sm text-white placeholder-gray-500 outline-none"
          />

          <select
            value={sort}
            onChange={(e) => setSort(e.target.value)}
            className="px-4 py-2 rounded-xl glass text-sm text-white outline-none"
          >
            {SORT_OPTIONS.map(opt => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
        </div>
      )}

      {/* Results */}
      {loading ? (
        <MediaSkeleton count={20} />
      ) : !hasSearched ? (
        <div className="flex flex-col items-center justify-center py-20">
          <SearchIcon className="w-16 h-16 text-gray-700 mb-4" />
          <p className="text-gray-500 text-lg">Start typing to search</p>
        </div>
      ) : items.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20">
          <p className="text-gray-400 text-lg">No results found</p>
          <p className="text-gray-600 text-sm mt-2">Try different keywords or filters</p>
        </div>
      ) : (
        <>
          <p className="text-sm text-gray-400 mb-4">{items.length} results</p>
          <MediaGrid items={items} />
        </>
      )}
    </div>
  );
}
