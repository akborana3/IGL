"""Telegram channel indexer — scan history, extract metadata, store in MongoDB."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, AsyncIterator, Dict, List, Optional

from telethon.tl.types import Message, MessageMediaDocument, MessageMediaPhoto
from telethon.errors import FloodWaitError

from app.database.connection import get_collection
from app.models.media import new_media_doc
from app.telethon_exec.client import get_channel, get_client, is_connected
from app.utils.helpers import (
    extract_tags,
    extract_title_from_filename,
    guess_category,
    slugify,
)

logger = logging.getLogger(__name__)


async def _iter_channel_messages(limit: int = 0) -> AsyncIterator[Message]:
    """Iterate through channel messages, newest first."""
    client = get_client()
    channel = get_channel()
    async for msg in client.iter_messages(channel, limit=limit or None):
        yield msg


def _extract_metadata(msg: Message) -> Optional[Dict[str, Any]]:
    """Extract media metadata from a Telegram message."""
    media = msg.media
    if media is None:
        return None

    if isinstance(media, MessageMediaPhoto):
        # Skip photos for now — focus on video/audio/document
        return None

    if not isinstance(media, MessageMediaDocument):
        return None

    doc = media.document
    if doc is None:
        return None

    filename = ""
    mime_type = ""
    file_size = 0
    duration = 0
    width = 0
    height = 0
    thumbnail_bytes = None

    for attr in doc.attributes:
        attr_class = type(attr).__name__
        if attr_class == "DocumentAttributeFilename":
            filename = attr.file_name or ""
        elif attr_class == "DocumentAttributeVideo":
            duration = getattr(attr, "duration", 0) or 0
            width = getattr(attr, "w", 0) or 0
            height = getattr(attr, "h", 0) or 0
        elif attr_class == "DocumentAttributeAudio":
            duration = getattr(attr, "duration", 0) or 0

    mime_type = doc.mime_type or ""
    file_size = doc.size or 0

    # Extract thumbnail if available
    if hasattr(doc, "thumbs") and doc.thumbs:
        # Store the smallest thumb size type; actual bytes fetched on demand
        thumbnail_bytes = None  # Will be fetched separately if needed

    caption = msg.message or ""
    title = extract_title_from_filename(filename) if filename else (caption[:80] if caption else f"Media {msg.id}")
    slug = slugify(title)
    category = guess_category(filename, mime_type)
    tags = extract_tags(filename, caption)

    return {
        "telegram_message_id": msg.id,
        "channel_id": msg.chat_id or 0,
        "title": title,
        "slug": slug,
        "caption": caption,
        "description": caption,
        "category": category,
        "tags": tags,
        "duration": duration,
        "width": width,
        "height": height,
        "file_size": file_size,
        "mime_type": mime_type,
        "thumbnail": None,  # Fetched on demand
        "upload_date": msg.date or datetime.now(timezone.utc),
        "filename": filename,
    }


async def _ensure_unique_slug(slug: str, exclude_msg_id: int) -> str:
    """Ensure slug uniqueness by appending a suffix if needed."""
    media_col = get_collection("media")
    base = slug
    suffix = 1
    while True:
        existing = await media_col.find_one({"slug": slug, "telegram_message_id": {"$ne": exclude_msg_id}})
        if not existing:
            return slug
        slug = f"{base}-{suffix}"
        suffix += 1


async def initial_scan() -> int:
    """Scan the entire channel and index all media. Returns count of new records."""
    if not is_connected():
        logger.warning("Telegram not connected — skipping initial scan")
        return 0

    media_col = get_collection("media")
    new_count = 0

    try:
        async for msg in _iter_channel_messages():
            metadata = _extract_metadata(msg)
            if metadata is None:
                continue

            # Check for duplicate
            existing = await media_col.find_one({"telegram_message_id": metadata["telegram_message_id"]})
            if existing:
                # Update caption if changed
                if existing.get("caption") != metadata["caption"]:
                    await media_col.update_one(
                        {"telegram_message_id": metadata["telegram_message_id"]},
                        {"$set": {"caption": metadata["caption"], "description": metadata["caption"], "updated_at": datetime.now(timezone.utc)}},
                    )
                continue

            # Ensure unique slug
            metadata["slug"] = await _ensure_unique_slug(metadata["slug"], metadata["telegram_message_id"])

            doc = new_media_doc(
                telegram_message_id=metadata["telegram_message_id"],
                channel_id=metadata["channel_id"],
                title=metadata["title"],
                slug=metadata["slug"],
                caption=metadata["caption"],
                description=metadata["description"],
                category=metadata["category"],
                tags=metadata["tags"],
                duration=metadata["duration"],
                width=metadata["width"],
                height=metadata["height"],
                file_size=metadata["file_size"],
                mime_type=metadata["mime_type"],
                thumbnail=metadata["thumbnail"],
                upload_date=metadata["upload_date"],
            )

            await media_col.insert_one(doc)
            new_count += 1

            if new_count % 50 == 0:
                logger.info("Indexed %d new media items...", new_count)

    except FloodWaitError as e:
        logger.warning("FloodWait: must wait %d seconds", e.seconds)
    except Exception as e:
        logger.error("Error during initial scan: %s", e)

    logger.info("Initial scan complete: %d new items indexed", new_count)
    await _rebuild_categories()
    return new_count


async def sync_new_messages() -> int:
    """Check for new messages since the last indexed one. Returns count of new records."""
    if not is_connected():
        return 0

    media_col = get_collection("media")
    new_count = 0

    try:
        # Get the latest indexed message ID
        latest = await media_col.find_one(sort=[("telegram_message_id", -1)])
        min_id = latest["telegram_message_id"] if latest else 0

        client = get_client()
        channel = get_channel()

        async for msg in client.iter_messages(channel, min_id=min_id):
            metadata = _extract_metadata(msg)
            if metadata is None:
                continue

            existing = await media_col.find_one({"telegram_message_id": metadata["telegram_message_id"]})
            if existing:
                continue

            metadata["slug"] = await _ensure_unique_slug(metadata["slug"], metadata["telegram_message_id"])

            doc = new_media_doc(
                telegram_message_id=metadata["telegram_message_id"],
                channel_id=metadata["channel_id"],
                title=metadata["title"],
                slug=metadata["slug"],
                caption=metadata["caption"],
                description=metadata["description"],
                category=metadata["category"],
                tags=metadata["tags"],
                duration=metadata["duration"],
                width=metadata["width"],
                height=metadata["height"],
                file_size=metadata["file_size"],
                mime_type=metadata["mime_type"],
                thumbnail=metadata["thumbnail"],
                upload_date=metadata["upload_date"],
            )

            await media_col.insert_one(doc)
            new_count += 1

    except FloodWaitError as e:
        logger.warning("FloodWait during sync: must wait %d seconds", e.seconds)
    except Exception as e:
        logger.error("Error during sync: %s", e)

    if new_count > 0:
        logger.info("Sync: %d new items", new_count)
        await _rebuild_categories()

    return new_count


async def _rebuild_categories() -> None:
    """Rebuild the categories collection from media data."""
    media_col = get_collection("media")
    cat_col = get_collection("categories")

    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
    ]
    async for group in media_col.aggregate(pipeline):
        name = group["_id"] or "Uncategorized"
        slug = slugify(name)
        await cat_col.update_one(
            {"slug": slug},
            {"$set": {"name": name, "slug": slug, "media_count": group["count"]}},
            upsert=True,
        )
