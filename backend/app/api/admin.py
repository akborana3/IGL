"""Admin API endpoints — authentication and management."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_admin
from app.schemas.admin import AdminLoginRequest, AdminLoginResponse
from app.schemas.media import MediaUpdate
from app.services.admin_service import (
    admin_dashboard,
    admin_delete_media,
    admin_feature_media,
    admin_update_media,
    authenticate_admin,
)
from app.services.analytics_service import get_analytics
from app.telethon_exec.indexer import sync_new_messages

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/login", response_model=AdminLoginResponse)
async def login(credentials: AdminLoginRequest) -> AdminLoginResponse:
    """Admin login — returns JWT token."""
    token = await authenticate_admin(credentials.username, credentials.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return AdminLoginResponse(access_token=token, username=credentials.username)


@router.get("/dashboard")
async def dashboard(admin: str = Depends(get_current_admin)) -> Dict[str, Any]:
    """Admin dashboard summary."""
    return await admin_dashboard()


@router.post("/media/update")
async def update_media_metadata(
    payload: MediaUpdate,
    slug: str,
    admin: str = Depends(get_current_admin),
) -> Dict[str, Any]:
    """Update media metadata (admin only)."""
    updates = payload.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
    result = await admin_update_media(slug, updates)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")
    return {"success": True, "data": result}


@router.post("/media/feature")
async def feature_media(
    slug: str,
    featured: bool = True,
    admin: str = Depends(get_current_admin),
) -> Dict[str, Any]:
    """Feature or unfeature media (admin only)."""
    result = await admin_feature_media(slug, featured)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")
    return {"success": True, "data": result}


@router.post("/media/delete")
async def delete_media_metadata(
    slug: str,
    admin: str = Depends(get_current_admin),
) -> Dict[str, Any]:
    """Delete a media metadata record (admin only). Does NOT delete from Telegram."""
    deleted = await admin_delete_media(slug)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")
    return {"success": True, "message": "Metadata deleted"}


@router.post("/sync")
async def trigger_sync(admin: str = Depends(get_current_admin)) -> Dict[str, Any]:
    """Manually trigger a sync of new Telegram messages (admin only)."""
    count = await sync_new_messages()
    return {"success": True, "new_items": count}


@router.get("/analytics")
async def analytics(admin: str = Depends(get_current_admin)) -> Dict[str, Any]:
    """Get analytics data (admin only)."""
    return await get_analytics()
