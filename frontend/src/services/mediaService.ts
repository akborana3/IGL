/** API service for media detail and related media. */

import api from "@/lib/api";
import type { MediaDetail, Media } from "@/types";

export async function fetchMediaDetail(slug: string): Promise<MediaDetail> {
  const { data } = await api.get<MediaDetail>(`/api/media/${slug}`);
  return data;
}

export async function fetchRelatedMedia(slug: string, limit: number = 10): Promise<Media[]> {
  const { data } = await api.get<{ items: Media[] }>(`/api/related/${slug}`, { params: { limit } });
  return data.items;
}
