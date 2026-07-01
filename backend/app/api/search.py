"""Search API endpoint with filters and sorting."""

from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, status

from app.services.search_service import search_media

router = APIRouter(prefix="/api", tags=["search"])


@router.get("/search")
async def search(
    q: str = "",
    page: int = 1,
    limit: int = 20,
    category: Optional[str] = None,
    year: Optional[int] = None,
    sort: str = "newest",
) -> Dict[str, Any]:
    """Search media by title, description, tags, and category.

    Supports filtering by category and year, plus sorting options:
    newest, oldest, most_viewed, most_downloaded, alphabetical.
    """
    try:
        result = await search_media(
            query=q,
            page=page,
            limit=limit,
            category=category,
            year=year,
            sort=sort,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {e}",
        )
