"""Media detail and related media API endpoints."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, status

from app.services.analytics_service import track_view
from app.services.media_service import get_media_by_slug, get_related_media

router = APIRouter(prefix="/api", tags=["media"])


@router.get("/media/{slug}")
async def media_detail(slug: str) -> Dict[str, Any]:
    """Get detailed information about a specific media item."""
    media = await get_media_by_slug(slug)
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")

    # Track view
    await track_view(slug)

    # Get related media
    related = await get_related_media(slug, limit=10)

    return {**media, "related": related}


@router.get("/related/{slug}")
async def related_media(slug: str, limit: int = 10) -> Dict[str, Any]:
    """Get media related to the given slug."""
    items = await get_related_media(slug, limit=limit)
    return {"items": items}
