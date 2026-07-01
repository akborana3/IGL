/** API endpoints and app constants. */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:7860";

export const API_BASE_URL = API_URL;

export const ENDPOINTS = {
  home: `${API_URL}/api/home`,
  trending: `${API_URL}/api/trending`,
  latest: `${API_URL}/api/latest`,
  categories: `${API_URL}/api/categories`,
  mediaDetail: (slug: string) => `${API_URL}/api/media/${slug}`,
  related: (slug: string) => `${API_URL}/api/related/${slug}`,
  search: `${API_URL}/api/search`,
  stream: (messageId: number) => `${API_URL}/api/stream/${messageId}`,
  download: (messageId: number) => `${API_URL}/api/download/${messageId}`,
  adminLogin: `${API_URL}/api/admin/login`,
  adminDashboard: `${API_URL}/api/admin/dashboard`,
  adminAnalytics: `${API_URL}/api/admin/analytics`,
  adminUpdateMedia: `${API_URL}/api/admin/media/update`,
  adminFeatureMedia: `${API_URL}/api/admin/media/feature`,
  adminSync: `${API_URL}/api/admin/sync`,
} as const;

export const SORT_OPTIONS = [
  { value: "newest", label: "Newest" },
  { value: "oldest", label: "Oldest" },
  { value: "most_viewed", label: "Most Viewed" },
  { value: "most_downloaded", label: "Most Downloaded" },
  { value: "alphabetical", label: "A-Z" },
] as const;

export const NAV_LINKS = [
  { href: "/", label: "Home" },
  { href: "/browse", label: "Browse" },
  { href: "/categories", label: "Categories" },
  { href: "/search", label: "Search" },
] as const;

export const APP_NAME = "Lumora";
export const APP_TAGLINE = "Premium Streaming, Redefined";
