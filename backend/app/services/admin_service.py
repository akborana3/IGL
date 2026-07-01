"""Admin service — authentication and admin operations."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.database.connection import get_collection
from app.services.media_service import _serialize, delete_media, set_featured, update_media

logger = logging.getLogger(__name__)


async def authenticate_admin(username: str, password: str) -> Optional[str]:
    """Authenticate admin and return a JWT token, or None if invalid."""
    if username != settings.admin_username:
        return None

    if not settings.admin_password_hash:
        # Fallback: compare plaintext (for initial setup only)
        if password != settings.admin_password_hash:
            return None
    else:
        if not verify_password(password, settings.admin_password_hash):
            return None

    token = create_access_token({"sub": username})
    return token


async def admin_update_media(slug: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Admin: update media metadata."""
    allowed_fields = {"title", "description", "caption", "category", "tags", "featured"}
    filtered = {k: v for k, v in updates.items() if k in allowed_fields}
    if not filtered:
        return None
    return await update_media(slug, filtered)


async def admin_feature_media(slug: str, featured: bool) -> Optional[Dict[str, Any]]:
    """Admin: feature or unfeature media."""
    return await set_featured(slug, featured)


async def admin_delete_media(slug: str) -> bool:
    """Admin: delete a media metadata record."""
    return await delete_media(slug)


async def admin_dashboard() -> Dict[str, Any]:
    """Get admin dashboard summary."""
    media_col = get_collection("media")
    total_media = await media_col.count_documents({})
    total_views_agg = await media_col.aggregate([{"$group": {"_id": None, "total": {"$sum": "$views"}}}]).to_list(1)
    total_downloads_agg = await media_col.aggregate([{"$group": {"_id": None, "total": {"$sum": "$downloads"}}}]).to_list(1)

    return {
        "total_media": total_media,
        "total_views": total_views_agg[0]["total"] if total_views_agg else 0,
        "total_downloads": total_downloads_agg[0]["total"] if total_downloads_agg else 0,
        "last_sync": datetime.now(timezone.utc).isoformat(),
        "sync_status": "idle",
    }
