/** Zustand store for favorites — persisted to localStorage. No login required. */

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { FavoriteItem } from "@/types";

interface FavoritesState {
  favorites: FavoriteItem[];
  addFavorite: (item: FavoriteItem) => void;
  removeFavorite: (slug: string) => void;
  isFavorite: (slug: string) => boolean;
  clearFavorites: () => void;
}

export const useFavoritesStore = create<FavoritesState>()(
  persist(
    (set, get) => ({
      favorites: [],

      addFavorite: (item) =>
        set((state) => {
          if (state.favorites.some((f) => f.slug === item.slug)) return state;
          return { favorites: [...state.favorites, item] };
        }),

      removeFavorite: (slug) =>
        set((state) => ({
          favorites: state.favorites.filter((f) => f.slug !== slug),
        })),

      isFavorite: (slug) => get().favorites.some((f) => f.slug === slug),

      clearFavorites: () => set({ favorites: [] }),
    }),
    { name: "ott-favorites" }
  )
);
