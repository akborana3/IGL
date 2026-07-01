"""Homepage service — assemble data for all homepage sections."""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from app.database.connection import get_collection
from app.services.media_service import _serialize

logger = logging.getLogger(__name__)


async def get_home_data() -> Dict[str, Any]:
    """Get all homepage data in a single response."""
    return {
        "hero": await get_hero_media(),
        "trending": await get_trending(limit=20),
        "recently_added": await get_recently_added(limit=20),
        "popular": await get_popular(limit=20),
        "top_rated": await get_top_rated(limit=20),
        "featured_collections": await get_featured(limit=20),
        "categories": await get_categories_summary(),
        "latest_uploads": await get_recently_added(limit=20),
    }


async def get_hero_media() -> List[Dict[str, Any]]:
    """Get featured media for the hero banner (up to 5 items)."""
    col = get_collection("media")
    cursor = col.find({"featured": True}).sort("views", -1).limit(5)
    items = [_serialize(doc) async for doc in cursor]

    # Fallback to most viewed if no featured items
    if not items:
        cursor = col.find().sort("views", -1).limit(5)
        items = [_serialize(doc) async for doc in cursor]

    return items


async def get_trending(limit: int = 20) -> List[Dict[str, Any]]:
    """Get trending media — most viewed in the last 30 days."""
    col = get_collection("media")
    from datetime import datetime, timedelta, timezone
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    cursor = col.find({"upload_date": {"$gte": thirty_days_ago}}).sort("views", -1).limit(limit)
    items = [_serialize(doc) async for doc in cursor]

    # Fallback to all-time most viewed
    if len(items) < limit:
        cursor = col.find().sort("views", -1).limit(limit)
        items = [_serialize(doc) async for doc in cursor]

    return items


async def get_recently_added(limit: int = 20) -> List[Dict[str, Any]]:
    """Get most recently added media."""
    col = get_collection("media")
    cursor = col.find().sort("upload_date", -1).limit(limit)
    return [_serialize(doc) async for doc in cursor]


async def get_popular(limit: int = 20) -> List[Dict[str, Any]]:
    """Get most popular media by views."""
    col = get_collection("media")
    cursor = col.find().sort("views", -1).limit(limit)
    return [_serialize(doc) async for doc in cursor]


async def get_top_rated(limit: int = 20) -> List[Dict[str, Any]]:
    """Get top-rated media (using views as a proxy for rating)."""
    col = get_collection("media")
    cursor = col.find({"views": {"$gt": 0}}).sort("views", -1).limit(limit)
    items = [_serialize(doc) async for doc in cursor]
    if len(items) < limit:
        cursor = col.find().sort("views", -1).limit(limit)
        items = [_serialize(doc) async for doc in cursor]
    return items


async def get_featured(limit: int = 20) -> List[Dict[str, Any]]:
    """Get featured media."""
    col = get_collection("media")
    cursor = col.find({"featured": True}).sort("views", -1).limit(limit)
    return [_serialize(doc) async for doc in cursor]


async def get_categories_summary() -> List[Dict[str, Any]]:
    """Get all categories with media counts."""
    col = get_collection("categories")
    cursor = col.find().sort("media_count", -1)
    return [_serialize(doc) async for doc in cursor]
