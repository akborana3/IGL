"""Streaming and download endpoints with HTTP Range support."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, Header, HTTPException, Request, status
from fastapi.responses import StreamingResponse

from app.core.config import settings
from app.services.analytics_service import track_download
from app.services.media_service import get_media_by_message_id, get_media_by_slug, increment_downloads, increment_views
from app.telethon_exec.streamer import get_media_size, stream_media_chunks
from app.utils.helpers import build_content_range, parse_range_header

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["stream"])


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
    media = await get_media_by_message_id(message_id)
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")

    file_size = media.get("file_size", 0)
    mime_type = media.get("mime_type", "application/octet-stream")

    # If we don't know the file size, try to get it from Telegram
    if file_size == 0:
        file_size = await get_media_size(message_id) or 0

    if file_size == 0:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to determine file size")

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


@router.get("/download/{message_id}")
async def download_media(
    message_id: int,
    range: Optional[str] = Header(None),
) -> StreamingResponse:
    """Download media from Telegram with HTTP Range support.

    Increments the download counter after successful transfer.
    """
    media = await get_media_by_message_id(message_id)
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")

    file_size = media.get("file_size", 0)
    mime_type = media.get("mime_type", "application/octet-stream")
    title = media.get("title", f"media_{message_id}")

    if file_size == 0:
        file_size = await get_media_size(message_id) or 0

    if file_size == 0:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to determine file size")

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
