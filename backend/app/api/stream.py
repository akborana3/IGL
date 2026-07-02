"""Streaming and download endpoints with HTTP Range support."""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional

from fastapi import APIRouter, Header, HTTPException, Request, status
from fastapi.responses import FileResponse, Response, StreamingResponse

from app.core.config import settings
from app.services.analytics_service import track_download
from app.services.media_service import get_media_by_message_id, get_media_by_slug, increment_downloads, increment_views
from app.services.thumbnail_service import get_thumbnail_path
from app.telethon_exec.streamer import get_media_size, stream_media_chunks
from app.utils.helpers import build_content_range, parse_range_header

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["stream"])


async def _resolve_media_info(message_id: int) -> dict:
    """Fetch media record and resolve file_size + mime_type.

    Raises HTTPException if media not found or file size cannot be determined.
    """
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


@router.head("/stream/{message_id}")
async def stream_media_head(
    message_id: int,
    range: Optional[str] = Header(None),
) -> Response:
    """HEAD request — return headers without streaming body.

    Vidstack and browsers send HEAD to check file size, range support,
    and content type before initiating the actual GET stream.
    """
    info = await _resolve_media_info(message_id)
    file_size = info["file_size"]
    mime_type = info["mime_type"]

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


@router.get("/stream/{message_id}")
async def stream_media(
    message_id: int,
    request: Request,
    range: Optional[str] = Header(None),
) -> StreamingResponse:
    """Stream media from Telegram with HTTP Range support.

    Returns 200 with full content if no Range header, or 206 Partial Content
    with the requested byte range.
    """
    info = await _resolve_media_info(message_id)
    media = info["media"]
    file_size = info["file_size"]
    mime_type = info["mime_type"]

    # Track view
    await increment_views(media["slug"])

    # Parse Range header
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

    # Calculate Telethon offset and limit
    offset = start
    limit = content_length

    return StreamingResponse(
        stream_media_chunks(message_id, offset=offset, limit=limit),
        status_code=status_code,
        headers=headers,
        media_type=mime_type,
    )


@router.get("/thumbnail/{message_id}")
async def get_thumbnail(message_id: int):
    """Serve a stored thumbnail image from HF Bucket storage.

    If the thumbnail doesn't exist in storage, returns 404.
    """
    filename = f"{message_id}.jpg"
    filepath = get_thumbnail_path(filename)
    if filepath is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thumbnail not found")
    return FileResponse(filepath, media_type="image/jpeg", headers={"Cache-Control": "public, max-age=86400"})


@router.get("/download/{message_id}")
async def download_media(
    message_id: int,
    range: Optional[str] = Header(None),
) -> StreamingResponse:
    """Download media from Telegram with HTTP Range support.

    Increments the download counter after successful transfer.
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

    # Build a filename from the title
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

    # Track download
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
