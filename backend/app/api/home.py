"""Home, trending, latest, and categories API endpoints."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, status

from app.services.homepage_service import (
    get_categories_summary,
    get_home_data,
    get_recently_added,
    get_trending,
)

router = APIRouter(prefix="/api", tags=["home"])


@router.get("/home")
async def home() -> Dict[str, Any]:
    """Get all homepage data in a single response."""
    try:
        return await get_home_data()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load home data: {e}",
        )


@router.get("/trending")
async def trending(limit: int = 20) -> Dict[str, Any]:
    """Get trending media."""
    items = await get_trending(limit=limit)
    return {"items": items}


@router.get("/latest")
async def latest(limit: int = 20) -> Dict[str, Any]:
    """Get recently added media."""
    items = await get_recently_added(limit=limit)
    return {"items": items}


@router.get("/categories")
async def categories() -> Dict[str, Any]:
    """Get all categories with media counts."""
    items = await get_categories_summary()
    return {"items": items}
