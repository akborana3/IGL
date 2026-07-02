/** Stream and download URL builders. */

import { ENDPOINTS } from "@/lib/constants";

export function getStreamUrl(messageId: number): string {
  return ENDPOINTS.stream(messageId);
}

export function getDownloadUrl(messageId: number): string {
  return ENDPOINTS.download(messageId);
}

/** Get stream URL + format info for conditional player selection.
 * Returns isMkv=true for MKV files so the frontend can use Artplayer.
 */
export function getStreamUrlWithFormat(messageId: number, mimeType: string): { url: string; isMkv: boolean } {
  const url = ENDPOINTS.stream(messageId);
  const isMkv = mimeType === "video/x-matroska" || mimeType === "video/x-matroska-3d";
  return { url, isMkv };
}
