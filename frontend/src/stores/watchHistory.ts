/** Zustand store for watch history — persisted to localStorage. No login required. */

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { WatchHistoryItem } from "@/types";

interface WatchHistoryState {
  history: WatchHistoryItem[];
  updateProgress: (item: WatchHistoryItem) => void;
  getProgress: (slug: string) => WatchHistoryItem | undefined;
  removeHistory: (slug: string) => void;
  clearHistory: () => void;
}

export const useWatchHistoryStore = create<WatchHistoryState>()(
  persist(
    (set, get) => ({
      history: [],

      updateProgress: (item) =>
        set((state) => {
          const filtered = state.history.filter((h) => h.slug !== item.slug);
          return { history: [item, ...filtered].slice(0, 50) };
        }),

      getProgress: (slug) => get().history.find((h) => h.slug === slug),

      removeHistory: (slug) =>
        set((state) => ({
          history: state.history.filter((h) => h.slug !== slug),
        })),

      clearHistory: () => set({ history: [] }),
    }),
    { name: "ott-watch-history" }
  )
);
