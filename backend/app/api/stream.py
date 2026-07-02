"""Streaming and download endpoints with HTTP Range support.

MKV files are automatically remuxed to fragmented MP4 via FFmpeg pipe.
MP4, WebM, and audio files are streamed directly (passthrough).
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, Header, HTTPException, Request, status
from fastapi.responses import FileResponse, Response, StreamingResponse

from app.core.config import settings
from app.services.analytics_service import track_download
from app.services.media_service import get_media_by_message_id, increment_downloads, increment_views
from app.services.thumbnail_service import get_thumbnail_path
from app.telethon_exec.streamer import get_media_size, stream_media_chunks, stream_remuxed_chunks
from app.utils.helpers import build_content_range, parse_range_header

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["stream"])

# MIME types that need FFmpeg remux → fMP4
_REMUX_MIME_TYPES = {"video/x-matroska", "video/x-matroska-3d"}

# Output MIME type after remux
_REMUX_OUTPUT_MIME = "video/mp4"


def _needs_remux(mime_type: str) -> bool:
    """Check if this MIME type needs FFmpeg remuxing."""
    return mime_type in _REMUX_MIME_TYPES


async def _resolve_media_info(message_id: int) -> dict:
    """Fetch media record and resolve file_size + mime_type."""
    media = await get_media_by_message_id(message_id)
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")

    file_size = media.get("file_size", 0)
    mime_type = media.get("mime_type", "application/octet-stream")

    if file_size == 0:
        file_size = await get_media_size(message_id) or 0

    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to determine file size",
        )

    return {"media": media, "file_size": file_size, "mime_type": mime_type}


# ---------------------------------------------------------------------------
# HEAD — return headers without body (player uses this to check capabilities)
# ---------------------------------------------------------------------------
@router.head("/stream/{message_id}")
async def stream_media_head(
    message_id: int,
    range: Optional[str] = Header(None),
) -> Response:
    """HEAD request — return headers without streaming body.

    For MKV files, reports Content-Type as video/mp4 because the GET
    endpoint will remux to fMP4. This ensures the player knows it can play it.
    """
    info = await _resolve_media_info(message_id)
    file_size = info["file_size"]
    mime_type = info["mime_type"]

    # For MKV, the GET endpoint remuxes to fMP4 — report as video/mp4
    if _needs_remux(mime_type):
        mime_type = _REMUX_OUTPUT_MIME

    try:
        start, end = parse_range_header(range or "", file_size)
    except ValueError:
        return Response(
            status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            headers={"Content-Range": f"bytes */{file_size}"},
        )

    is_partial = range is not None
    status_code = 206 if is_partial else 200
    content_length = end - start + 1

    headers: Dict[str, str] = {
        "Accept-Ranges": "bytes",
        "Content-Length": str(content_length),
        "Content-Type": mime_type,
        "Cache-Control": "public, max-age=3600",
    }

    if is_partial:
        headers["Content-Range"] = build_content_range(start, end, file_size)

    return Response(status_code=status_code, headers=headers, media_type=mime_type)


# ---------------------------------------------------------------------------
# GET stream — direct passthrough OR FFmpeg remux
# ---------------------------------------------------------------------------
@router.get("/stream/{message_id}")
async def stream_media(
    message_id: int,
    request: Request,
    range: Optional[str] = Header(None),
) -> StreamingResponse:
    """Stream media from Telegram.

    - MP4/WebM/audio: direct passthrough with HTTP Range support
    - MKV: FFmpeg remux to fragmented MP4 (codec copy, no re-encode)
    """
    info = await _resolve_media_info(message_id)
    media = info["media"]
    file_size = info["file_size"]
    mime_type = info["mime_type"]

    # Track view
    await increment_views(media["slug"])

    # ---- MKV path: remux to fMP4 via FFmpeg ----
    if _needs_remux(mime_type):
        logger.info("Remuxing MKV message %d → fMP4", message_id)

        headers = {
            "Accept-Ranges": "bytes",
            "Content-Type": _REMUX_OUTPUT_MIME,
            "Cache-Control": "no-store",
            "X-Content-Type-Options": "nosniff",
        }

        return StreamingResponse(
            stream_remuxed_chunks(message_id),
            status_code=200,
            headers=headers,
            media_type=_REMUX_OUTPUT_MIME,
        )

    # ---- Direct passthrough path (MP4, WebM, audio) ----
    try:
        start, end = parse_range_header(range or "", file_size)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            detail="Requested range not satisfiable",
            headers={"Content-Range": f"bytes */{file_size}"},
        )

    is_partial = (range is not None)
    status_code = 206 if is_partial else 200
    content_length = end - start + 1

    headers = {
        "Accept-Ranges": "bytes",
        "Content-Length": str(content_length),
        "Content-Type": mime_type,
        "Cache-Control": "no-store",
    }

    if is_partial:
        headers["Content-Range"] = build_content_range(start, end, file_size)

    offset = start
    limit = content_length

    return StreamingResponse(
        stream_media_chunks(message_id, offset=offset, limit=limit),
        status_code=status_code,
        headers=headers,
        media_type=mime_type,
    )


# ---------------------------------------------------------------------------
# Thumbnail
# ---------------------------------------------------------------------------
@router.get("/thumbnail/{message_id}")
async def get_thumbnail(message_id: int):
    """Serve a stored thumbnail image from HF Bucket storage."""
    filename = f"{message_id}.jpg"
    filepath = get_thumbnail_path(filename)
    if filepath is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thumbnail not found")
    return FileResponse(filepath, media_type="image/jpeg", headers={"Cache-Control": "public, max-age=86400"})


# ---------------------------------------------------------------------------
# Download — always direct passthrough (original file, no remux)
# ---------------------------------------------------------------------------
@router.get("/download/{message_id}")
async def download_media(
    message_id: int,
    range: Optional[str] = Header(None),
) -> StreamingResponse:
    """Download media from Telegram with HTTP Range support.

    Always serves the original file (no remux). Increments download counter.
    """
    info = await _resolve_media_info(message_id)
    media = info["media"]
    file_size = info["file_size"]
    mime_type = info["mime_type"]
    title = media.get("title", f"media_{message_id}")

    try:
        start, end = parse_range_header(range or "", file_size)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            detail="Requested range not satisfiable",
            headers={"Content-Range": f"bytes */{file_size}"},
        )

    is_partial = (range is not None)
    status_code = 206 if is_partial else 200
    content_length = end - start + 1

    ext_map = {
        "video/mp4": ".mp4",
        "video/webm": ".webm",
        "video/x-matroska": ".mkv",
        "audio/mpeg": ".mp3",
        "audio/mp4": ".m4a",
        "audio/ogg": ".ogg",
    }
    ext = ext_map.get(mime_type, "")
    filename = f"{title}{ext}"

    headers = {
        "Accept-Ranges": "bytes",
        "Content-Length": str(content_length),
        "Content-Type": mime_type,
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Cache-Control": "no-store",
    }

    if is_partial:
        headers["Content-Range"] = build_content_range(start, end, file_size)

    await track_download(media["slug"])
    await increment_downloads(media["slug"])

    offset = start
    limit = content_length

    return StreamingResponse(
        stream_media_chunks(message_id, offset=offset, limit=limit),
        status_code=status_code,
        headers=headers,
        media_type=mime_type,
    )
