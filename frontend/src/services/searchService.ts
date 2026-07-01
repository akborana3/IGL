/** API service for search with filters. */

import api from "@/lib/api";
import type { SearchResult } from "@/types";

export interface SearchParams {
  q?: string;
  page?: number;
  limit?: number;
  category?: string;
  year?: number;
  sort?: string;
}

export async function searchMedia(params: SearchParams): Promise<SearchResult> {
  const { data } = await api.get<SearchResult>("/api/search", { params });
  return data;
}
