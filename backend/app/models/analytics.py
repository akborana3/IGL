"""Analytics document model."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional


def new_analytics_doc(
    media_id: str,
    event_type: str,  # "view" or "download"
) -> dict:
    return {
        "media_id": media_id,
        "event_type": event_type,
        "date": datetime.now(timezone.utc),
    }


def new_daily_summary(date: datetime, total_views: int = 0, total_downloads: int = 0) -> dict:
    return {
        "date": date,
        "total_views": total_views,
        "total_downloads": total_downloads,
    }
