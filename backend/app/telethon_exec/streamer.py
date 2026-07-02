"""Chunked MTProto streaming — read media from Telegram and stream to HTTP clients.

Optimised for:
- Faster startup (message cache avoids redundant API calls)
- Lower latency (1 MB chunks, prefetch)
- Better seeking (cached message objects, offset-aware reads)
- MKV remux to fMP4 via FFmpeg pipe (codec copy, no re-encode)
"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import AsyncIterator, Optional

from telethon.errors import FloodWaitError

from app.core.config import settings
from app.telethon_exec.client import get_channel, get_client, is_connected

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Message cache — avoids calling get_messages() on every Range request
# ---------------------------------------------------------------------------
_message_cache: dict[int, tuple[float, any]] = {}
_CACHE_TTL = settings.message_cache_ttl


async def _get_cached_message(telegram_message_id: int):
    """Return a cached message object or fetch from Telegram."""
    now = time.monotonic()
    cached = _message_cache.get(telegram_message_id)
    if cached and (now - cached[0]) < _CACHE_TTL:
        return cached[1]

    client = get_client()
    channel = get_channel()
    msg = await client.get_messages(channel, ids=telegram_message_id)
    if msg is not None:
        _message_cache[telegram_message_id] = (now, msg)
    return msg


def clear_message_cache(telegram_message_id: int | None = None) -> None:
    """Clear the message cache for one item or all."""
    if telegram_message_id is not None:
        _message_cache.pop(telegram_message_id, None)
    else:
        _message_cache.clear()


# ---------------------------------------------------------------------------
# Direct streaming — passthrough chunks from Telegram to HTTP client
# ---------------------------------------------------------------------------
async def stream_media_chunks(
    telegram_message_id: int,
    offset: int = 0,
    limit: int = 0,
    chunk_size: int = 0,
) -> AsyncIterator[bytes]:
    """Async generator that yields media bytes from Telegram in chunks.

    Uses a cached message object to avoid redundant API calls during seeking.
    """
    if not is_connected():
        raise RuntimeError("Telegram client not connected")

    client = get_client()
    cs = chunk_size or settings.chunk_size

    try:
        msg = await _get_cached_message(telegram_message_id)
        if msg is None or msg.media is None:
            raise FileNotFoundError(f"Message {telegram_message_id} has no media")

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


# ---------------------------------------------------------------------------
# FFmpeg remux — MKV → fragmented MP4 (codec copy, no re-encode)
# ---------------------------------------------------------------------------
async def stream_remuxed_chunks(
    telegram_message_id: int,
    chunk_size: int = 0,
) -> AsyncIterator[bytes]:
    """Read MKV from Telegram, pipe through FFmpeg, yield fMP4 chunks.

    FFmpeg command:
        ffmpeg -i pipe:0 -c copy -movflags frag_keyframe+empty_moov+default_base_moof -f mp4 pipe:1

    This is a **remux** (container change only) — no decoding or encoding.
    CPU usage is minimal. Latency is ~1-2 seconds for FFmpeg to buffer
    enough data before producing the first fMP4 segment.
    """
    if not is_connected():
        raise RuntimeError("Telegram client not connected")

    client = get_client()
    cs = chunk_size or settings.chunk_size

    # Build FFmpeg command
    cmd = [
        settings.ffmpeg_path,
        "-hide_banner",
        "-loglevel", "error",
        "-probesize", "32768",          # fast probe — don't scan entire file
        "-analyzeduration", "0",        # skip analysis (we know it's MKV)
        "-i", "pipe:0",
        "-c", "copy",                   # codec copy — NO re-encoding
        "-movflags", "frag_keyframe+empty_moov+default_base_moof",
        "-f", "mp4",
        "pipe:1",
    ]

    proc = None
    try:
        msg = await _get_cached_message(telegram_message_id)
        if msg is None or msg.media is None:
            raise FileNotFoundError(f"Message {telegram_message_id} has no media")

        # Start FFmpeg subprocess
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        # Task: feed Telegram chunks → FFmpeg stdin
        async def _feed_ffmpeg():
            try:
                async for chunk in client.iter_download(
                    msg.media,
                    offset=0,
                    limit=None,
                    chunk_size=cs,
                ):
                    if not chunk:
                        break
                    proc.stdin.write(chunk)
                    await proc.stdin.drain()
            except Exception as e:
                logger.error("Feed error for %d: %s", telegram_message_id, e)
            finally:
                if proc.stdin:
                    try:
                        proc.stdin.close()
                    except Exception:
                        pass

        feeder = asyncio.create_task(_feed_ffmpeg())

        # Yield FFmpeg stdout chunks to HTTP client
        while True:
            data = await proc.stdout.read(cs)
            if not data:
                break
            yield data

        # Wait for feeder to finish
        await feeder
        await proc.wait()

    except FloodWaitError as e:
        logger.warning("FloodWait during remux: must wait %d seconds", e.seconds)
        raise
    except Exception as e:
        logger.error("Error remuxing media %d: %s", telegram_message_id, e)
        raise
    finally:
        if proc and proc.returncode is None:
            try:
                proc.kill()
            except Exception:
                pass


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
async def get_media_size(telegram_message_id: int) -> Optional[int]:
    """Get the file size of the media attached to a Telegram message."""
    if not is_connected():
        return None

    try:
        msg = await _get_cached_message(telegram_message_id)
        if msg is None or msg.media is None:
            return None
        doc = msg.media.document if hasattr(msg.media, "document") else None
        if doc:
            return doc.size
    except Exception as e:
        logger.error("Error getting media size for %d: %s", telegram_message_id, e)
    return None


async def download_thumbnail_bytes(telegram_message_id: int) -> Optional[bytes]:
    """Download the thumbnail bytes for a Telegram media message."""
    if not is_connected():
        return None

    client = get_client()

    try:
        msg = await _get_cached_message(telegram_message_id)
        if msg is None or msg.media is None:
            return None
        thumbnail = await client.download_media(msg, thumb=True, file=bytes)
        return thumbnail
    except Exception as e:
        logger.error("Error fetching thumbnail for %d: %s", telegram_message_id, e)
        return None


# Keep backward-compatible alias
get_media_thumbnail = download_thumbnail_bytes
