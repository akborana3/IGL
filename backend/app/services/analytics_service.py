"""Analytics service — track views/downloads and aggregate stats."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from app.database.connection import get_collection
from app.models.analytics import new_analytics_doc
from app.services.media_service import _serialize

logger = logging.getLogger(__name__)


async def track_view(media_slug: str) -> None:
    """Record a view event."""
    analytics_col = get_collection("analytics")
    await analytics_col.insert_one(new_analytics_doc(media_slug, "view"))


async def track_download(media_slug: str) -> None:
    """Record a download event."""
    analytics_col = get_collection("analytics")
    await analytics_col.insert_one(new_analytics_doc(media_slug, "download"))


async def get_analytics() -> Dict[str, Any]:
    """Get aggregated analytics for the admin dashboard."""
    media_col = get_collection("media")
    analytics_col = get_collection("analytics")
    cat_col = get_collection("categories")

    total_media = await media_col.count_documents({})
    total_views_agg = await media_col.aggregate([{"$group": {"_id": None, "total": {"$sum": "$views"}}}]).to_list(1)
    total_downloads_agg = await media_col.aggregate([{"$group": {"_id": None, "total": {"$sum": "$downloads"}}}]).to_list(1)
    featured_count = await media_col.count_documents({"featured": True})
    categories_count = await cat_col.count_documents({})

    total_views = total_views_agg[0]["total"] if total_views_agg else 0
    total_downloads = total_downloads_agg[0]["total"] if total_downloads_agg else 0

    # Daily stats for last 7 days
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    daily_cursor = analytics_col.aggregate([
        {"$match": {"date": {"$gte": seven_days_ago}}},
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$date"}},
            "views": {"$sum": {"$cond": [{"$eq": ["$event_type", "view"]}, 1, 0]}},
            "downloads": {"$sum": {"$cond": [{"$eq": ["$event_type", "download"]}, 1, 0]}},
        }},
        {"$sort": {"_id": 1}},
    ])
    daily = [
        {"date": doc["_id"], "total_views": doc["views"], "total_downloads": doc["downloads"]}
        async for doc in daily_cursor
    ]

    # Top media by views
    top_cursor = media_col.find().sort("views", -1).limit(10)
    top_media = [
        {"title": doc.get("title", ""), "slug": doc.get("slug", ""), "views": doc.get("views", 0), "downloads": doc.get("downloads", 0)}
        async for doc in top_cursor
    ]

    return {
        "summary": {
            "total_media": total_media,
            "total_views": total_views,
            "total_downloads": total_downloads,
            "featured_count": featured_count,
            "categories_count": categories_count,
        },
        "daily": daily,
        "top_media": top_media,
    }
