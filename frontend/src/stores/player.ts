/** Zustand store for player state. */

import { create } from "zustand";
import { persist } from "zustand/middleware";

interface PlayerState {
  theaterMode: boolean;
  volume: number;
  muted: boolean;
  playbackSpeed: number;
  setTheaterMode: (v: boolean) => void;
  setVolume: (v: number) => void;
  setMuted: (v: boolean) => void;
  setPlaybackSpeed: (v: number) => void;
}

export const usePlayerStore = create<PlayerState>()(
  persist(
    (set) => ({
      theaterMode: false,
      volume: 1,
      muted: false,
      playbackSpeed: 1,

      setTheaterMode: (v) => set({ theaterMode: v }),
      setVolume: (v) => set({ volume: v }),
      setMuted: (v) => set({ muted: v }),
      setPlaybackSpeed: (v) => set({ playbackSpeed: v }),
    }),
    { name: "ott-player" }
  )
);
