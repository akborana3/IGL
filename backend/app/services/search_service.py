"""Search service — full-text search with filters and sorting."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from app.database.connection import get_collection
from app.services.media_service import _serialize

logger = logging.getLogger(__name__)


async def search_media(
    query: str = "",
    page: int = 1,
    limit: int = 20,
    category: Optional[str] = None,
    year: Optional[int] = None,
    sort: str = "newest",
) -> Dict[str, Any]:
    """Search media by title, description, caption, tags, and category.

    Supports filtering by category and year, plus multiple sort options.
    """
    col = get_collection("media")
    mongo_query: Dict[str, Any] = {}

    # Text search
    if query.strip():
        mongo_query["$text"] = {"$search": query}

    # Category filter
    if category:
        mongo_query["category"] = category

    # Year filter (search in tags which may contain year strings)
    if year:
        mongo_query["tags"] = {"$in": [str(year)]}

    sort_map = {
        "newest": [("upload_date", -1)],
        "oldest": [("upload_date", 1)],
        "most_viewed": [("views", -1)],
        "most_downloaded": [("downloads", -1)],
        "alphabetical": [("title", 1)],
    }
    sort_list = sort_map.get(sort, sort_map["newest"])

    total = await col.count_documents(mongo_query)
    skip = (page - 1) * limit
    cursor = col.find(mongo_query).sort(sort_list).skip(skip).limit(limit)
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
