"""Media document model — represents one indexed Telegram message."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional


class MediaDocument:
    """Field names for the media collection. Not an ORM — used as a reference."""

    telegram_message_id: int
    channel_id: int
    title: str
    description: str
    caption: str
    slug: str
    category: str
    tags: List[str]
    duration: int  # seconds
    width: int
    height: int
    file_size: int  # bytes
    mime_type: str
    thumbnail: Optional[str]  # base64 or URL
    upload_date: datetime
    views: int
    downloads: int
    featured: bool
    created_at: datetime
    updated_at: datetime


def new_media_doc(
    telegram_message_id: int,
    channel_id: int,
    title: str,
    slug: str,
    caption: str = "",
    description: str = "",
    category: str = "Uncategorized",
    tags: Optional[List[str]] = None,
    duration: int = 0,
    width: int = 0,
    height: int = 0,
    file_size: int = 0,
    mime_type: str = "",
    thumbnail: Optional[str] = None,
    upload_date: Optional[datetime] = None,
) -> dict:
    now = datetime.now(timezone.utc)
    return {
        "telegram_message_id": telegram_message_id,
        "channel_id": channel_id,
        "title": title,
        "description": description,
        "caption": caption,
        "slug": slug,
        "category": category,
        "tags": tags or [],
        "duration": duration,
        "width": width,
        "height": height,
        "file_size": file_size,
        "mime_type": mime_type,
        "thumbnail": thumbnail,
        "upload_date": upload_date or now,
        "views": 0,
        "downloads": 0,
        "featured": False,
        "created_at": now,
        "updated_at": now,
    }
