/** API service for homepage data. */

import api from "@/lib/api";
import type { HomeData, Media, Category } from "@/types";

export async function fetchHomeData(): Promise<HomeData> {
  const { data } = await api.get<HomeData>("/api/home");
  return data;
}

export async function fetchTrending(limit: number = 20): Promise<Media[]> {
  const { data } = await api.get<{ items: Media[] }>("/api/trending", { params: { limit } });
  return data.items;
}

export async function fetchLatest(limit: number = 20): Promise<Media[]> {
  const { data } = await api.get<{ items: Media[] }>("/api/latest", { params: { limit } });
  return data.items;
}

export async function fetchCategories(): Promise<Category[]> {
  const { data } = await api.get<{ items: Category[] }>("/api/categories");
  return data.items;
}
