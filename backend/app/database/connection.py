"""Async MongoDB connection management using Motor."""

from __future__ import annotations

import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

logger = logging.getLogger(__name__)

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None


async def connect_db() -> None:
    """Initialise the Motor client and create indexes."""
    global _client, _db
    _client = AsyncIOMotorClient(settings.mongo_url)
    _db = _client[settings.mongo_db]
    await _client.admin.command("ping")
    logger.info("MongoDB connected: %s", settings.mongo_db)
    await _ensure_indexes()


async def disconnect_db() -> None:
    """Close the Motor client."""
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        logger.info("MongoDB disconnected")


def get_db() -> AsyncIOMotorDatabase:
    if _db is None:
        raise RuntimeError("Database not initialised. Call connect_db() first.")
    return _db


def get_collection(name: str):
    return get_db()[name]


async def _ensure_indexes() -> None:
    """Create indexes on frequently queried fields."""
    db = get_db()

    await db.media.create_index("telegram_message_id", unique=True)
    await db.media.create_index("slug", unique=True)
    await db.media.create_index("category")
    await db.media.create_index("featured")
    await db.media.create_index("upload_date")
    await db.media.create_index([("title", "text"), ("description", "text"), ("tags", "text")])
    await db.media.create_index("views")
    await db.media.create_index("downloads")

    await db.categories.create_index("slug", unique=True)

    await db.analytics.create_index("date")
    await db.analytics.create_index("media_id")

    logger.info("MongoDB indexes ensured")
