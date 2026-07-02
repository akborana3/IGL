"""Thumbnail storage service — saves thumbnails to HF Bucket mount and serves them."""

from __future__ import annotations

import logging
import os
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


def _ensure_storage_dir() -> str:
    """Ensure the thumbnail storage directory exists. Returns the path."""
    path = settings.storage_path
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        logger.warning("Could not create storage dir %s: %s", path, e)
    return path


def save_thumbnail(telegram_message_id: int, thumbnail_bytes: bytes, ext: str = "jpg") -> Optional[str]:
    """Save thumbnail bytes to the HF Bucket mount.

    Returns the relative path (e.g. "12345.jpg") or None on failure.
    The full filesystem path is storage_path / relative_path.
    """
    if not thumbnail_bytes:
        return None

    storage_dir = _ensure_storage_dir()
    filename = f"{telegram_message_id}.{ext}"
    filepath = os.path.join(storage_dir, filename)

    try:
        with open(filepath, "wb") as f:
            f.write(thumbnail_bytes)
        logger.info("Thumbnail saved: %s (%d bytes)", filepath, len(thumbnail_bytes))
        return filename
    except Exception as e:
        logger.error("Failed to save thumbnail %s: %s", filepath, e)
        return None


def get_thumbnail_path(filename: str) -> Optional[str]:
    """Get the full filesystem path for a stored thumbnail."""
    if not filename:
        return None
    filepath = os.path.join(settings.storage_path, filename)
    if os.path.exists(filepath):
        return filepath
    return None


def get_thumbnail_url(filename: str) -> Optional[str]:
    """Get the public URL for a thumbnail if storage_url is configured."""
    if not filename:
        return None
    if settings.storage_url:
        return f"{settings.storage_url.rstrip('/')}/{filename}"
    return None


def thumbnail_exists(telegram_message_id: int, ext: str = "jpg") -> bool:
    """Check if a thumbnail file already exists in storage."""
    filename = f"{telegram_message_id}.{ext}"
    filepath = os.path.join(settings.storage_path, filename)
    return os.path.exists(filepath)