/** Stream and download URL builders. */

import { ENDPOINTS } from "@/lib/constants";

export function getStreamUrl(messageId: number): string {
  return ENDPOINTS.stream(messageId);
}

export function getDownloadUrl(messageId: number): string {
  return ENDPOINTS.download(messageId);
}
