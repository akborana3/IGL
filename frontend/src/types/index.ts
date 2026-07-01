/** TypeScript types for the OTT streaming platform. */

export interface Media {
  id: string;
  telegram_message_id: number;
  title: string;
  slug: string;
  category: string;
  tags: string[];
  duration: number;
  width: number;
  height: number;
  file_size: number;
  mime_type: string;
  thumbnail: string | null;
  upload_date: string;
  views: number;
  downloads: number;
  featured: boolean;
  description: string;
  caption: string;
}

export interface MediaDetail extends Media {
  channel_id: number;
  created_at: string;
  updated_at: string;
  related: Media[];
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  icon: string;
  description: string;
  media_count: number;
}

export interface PaginationInfo {
  page: number;
  limit: number;
  total: number;
  total_pages: number;
  has_next: boolean;
}

export interface PaginatedResponse<T> {
  items: T[];
  pagination: PaginationInfo;
}

export interface HomeData {
  hero: Media[];
  trending: Media[];
  recently_added: Media[];
  popular: Media[];
  top_rated: Media[];
  featured_collections: Media[];
  categories: Category[];
  latest_uploads: Media[];
}

export interface SearchResult extends PaginatedResponse<Media> {}

export interface AnalyticsSummary {
  total_media: number;
  total_views: number;
  total_downloads: number;
  featured_count: number;
  categories_count: number;
}

export interface DailyAnalytics {
  date: string;
  total_views: number;
  total_downloads: number;
}

export interface AnalyticsResponse {
  summary: AnalyticsSummary;
  daily: DailyAnalytics[];
  top_media: Array<{
    title: string;
    slug: string;
    views: number;
    downloads: number;
  }>;
}

export interface WatchHistoryItem {
  slug: string;
  title: string;
  thumbnail: string | null;
  progress: number; // 0-1
  position: number; // seconds
  duration: number; // seconds
  lastWatched: number; // timestamp
}

export interface FavoriteItem {
  slug: string;
  title: string;
  thumbnail: string | null;
  addedAt: number;
}
