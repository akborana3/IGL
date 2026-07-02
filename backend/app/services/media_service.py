"""Media service — CRUD operations, views/downloads increment, related media."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from bson import ObjectId

from app.database.connection import get_collection

logger = logging.getLogger(__name__)


def _serialize(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a MongoDB document to a serializable dict."""
    if doc is None:
        return {}
    doc = dict(doc)
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc


async def get_media_by_slug(slug: str) -> Optional[Dict[str, Any]]:
    """Fetch a single media item by slug."""
    col = get_collection("media")
    doc = await col.find_one({"slug": slug})
    return _serialize(doc) if doc else None


async def get_media_by_message_id(msg_id: int) -> Optional[Dict[str, Any]]:
    """Fetch a single media item by Telegram message ID."""
    col = get_collection("media")
    doc = await col.find_one({"telegram_message_id": msg_id})
    return _serialize(doc) if doc else None


async def get_media_list(
    page: int = 1,
    limit: int = 20,
    category: Optional[str] = None,
    sort: str = "newest",
) -> Dict[str, Any]:
    """Get a paginated, filtered, sorted list of media."""
    col = get_collection("media")
    query: Dict[str, Any] = {}
    if category:
        query["category"] = category

    sort_map = {
        "newest": [("upload_date", -1)],
        "oldest": [("upload_date", 1)],
        "most_viewed": [("views", -1)],
        "most_downloaded": [("downloads", -1)],
        "alphabetical": [("title", 1)],
    }
    sort_list = sort_map.get(sort, sort_map["newest"])

    total = await col.count_documents(query)
    skip = (page - 1) * limit
    cursor = col.find(query).sort(sort_list).skip(skip).limit(limit)
    items = [_serialize(doc) async for doc in cursor]

    total_pages = (total + limit - 1) // limit if limit > 0 else 0
    return {
        "items": items,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
        },
    }


async def increment_views(slug: str) -> None:
    """Increment the view count for a media item."""
    col = get_collection("media")
    await col.update_one({"slug": slug}, {"$inc": {"views": 1}})


async def increment_downloads(slug: str) -> None:
    """Increment the download count for a media item."""
    col = get_collection("media")
    await col.update_one({"slug": slug}, {"$inc": {"downloads": 1}})


async def update_media(slug: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update media metadata."""
    col = get_collection("media")
    updates["updated_at"] = datetime.now(timezone.utc)
    result = await col.find_one_and_update(
        {"slug": slug},
        {"$set": updates},
        return_document=True,
    )
    return _serialize(result) if result else None


async def set_featured(slug: str, featured: bool) -> Optional[Dict[str, Any]]:
    """Set or unset the featured flag on a media item."""
    col = get_collection("media")
    result = await col.find_one_and_update(
        {"slug": slug},
        {"$set": {"featured": featured, "updated_at": datetime.now(timezone.utc)}},
        return_document=True,
    )
    return _serialize(result) if result else None


async def delete_media(slug: str) -> bool:
    """Delete a media metadata record (does NOT delete from Telegram)."""
    col = get_collection("media")
    result = await col.delete_one({"slug": slug})
    return result.deleted_count > 0


async def get_related_media(slug: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Get related media based on category and tags."""
    col = get_collection("media")
    media = await col.find_one({"slug": slug})
    if not media:
        return []

    category = media.get("category", "")
    tags = media.get("tags", [])

    # First try same category + matching tags
    query = {
        "slug": {"$ne": slug},
        "$or": [
            {"category": category},
            {"tags": {"$in": tags}} if tags else {},
        ],
    }
    cursor = col.find(query).limit(limit)
    items = [_serialize(doc) async for doc in cursor]

    # Fallback to same category only
    if len(items) < limit:
        existing_ids = [item["slug"] for item in items] + [slug]
        cursor = col.find({"slug": {"$nin": existing_ids}, "category": category}).limit(limit - len(items))
        fallback = [_serialize(doc) async for doc in cursor]
        items.extend(fallback)

    return items[:limit]
