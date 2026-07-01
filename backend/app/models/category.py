"""Category document model."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional


def new_category_doc(
    name: str,
    slug: str,
    icon: str = "",
    description: str = "",
    media_count: int = 0,
) -> dict:
    return {
        "name": name,
        "slug": slug,
        "icon": icon,
        "description": description,
        "media_count": media_count,
        "created_at": datetime.now(timezone.utc),
    }
