"""Chunked MTProto streaming — read media from Telegram and stream to HTTP clients."""

from __future__ import annotations

import asyncio
import logging
from typing import AsyncIterator, Optional

from telethon.errors import FloodWaitError

from app.core.config import settings
from app.telethon_exec.client import get_channel, get_client, is_connected

logger = logging.getLogger(__name__)


async def stream_media_chunks(
    telegram_message_id: int,
    offset: int = 0,
    limit: int = 0,
    chunk_size: int = 0,
) -> AsyncIterator[bytes]:
    """Async generator that yields media bytes from Telegram in chunks.

    Args:
        telegram_message_id: The Telegram message ID containing the media.
        offset: Byte offset to start reading from (for Range requests).
        limit: Maximum bytes to read (0 = read to end).
        chunk_size: Size of each chunk to yield.
    """
    if not is_connected():
        raise RuntimeError("Telegram client not connected")

    client = get_client()
    channel = get_channel()
    cs = chunk_size or settings.chunk_size

    try:
        # Get the message and its media
        msg = await client.get_messages(channel, ids=telegram_message_id)
        if msg is None or msg.media is None:
            raise FileNotFoundError(f"Message {telegram_message_id} has no media")

        # Use Telethon's iter_download to read in chunks
        async for chunk in client.iter_download(
            msg.media,
            offset=offset,
            limit=limit if limit > 0 else None,
            chunk_size=cs,
        ):
            if chunk:
                yield chunk
            else:
                break

    except FloodWaitError as e:
        logger.warning("FloodWait during stream: must wait %d seconds", e.seconds)
        raise
    except Exception as e:
        logger.error("Error streaming media %d: %s", telegram_message_id, e)
        raise


async def get_media_size(telegram_message_id: int) -> Optional[int]:
    """Get the file size of the media attached to a Telegram message."""
    if not is_connected():
        return None

    client = get_client()
    channel = get_channel()

    msg = await client.get_messages(channel, ids=telegram_message_id)
    if msg is None or msg.media is None:
        return None

    doc = msg.media.document if hasattr(msg.media, "document") else None
    if doc:
        return doc.size
    return None


async def download_thumbnail_bytes(telegram_message_id: int) -> Optional[bytes]:
    """Download the thumbnail bytes for a Telegram media message.

    Returns raw bytes of the thumbnail image, or None if no thumbnail available.
    """
    if not is_connected():
        return None

    client = get_client()
    channel = get_channel()

    msg = await client.get_messages(channel, ids=telegram_message_id)
    if msg is None or msg.media is None:
        return None

    try:
        # Download just the thumbnail (small preview image)
        thumbnail = await client.download_media(msg, thumb=True, file=bytes)
        return thumbnail
    except Exception as e:
        logger.error("Error fetching thumbnail for %d: %s", telegram_message_id, e)
        return None


# Keep backward-compatible alias
get_media_thumbnail = download_thumbnail_bytes