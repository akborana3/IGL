"""Async MongoDB connection management using Motor."""

from __future__ import annotations

import asyncio
import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

logger = logging.getLogger(__name__)

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None
_db_connected: bool = False


async def connect_db() -> None:
    """Initialise the Motor client. Non-fatal if MongoDB is unavailable."""
    global _client, _db, _db_connected

    _client = AsyncIOMotorClient(
        settings.mongo_url,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
        socketTimeoutMS=20000,
    )
    _db = _client[settings.mongo_db]

    # Try to connect, but don't crash the app if MongoDB is unavailable
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            await _client.admin.command("ping")
            _db_connected = True
            logger.info("MongoDB connected: %s", settings.mongo_db)
            await _ensure_indexes()
            return
        except Exception as e:
            logger.warning("MongoDB connection attempt %d/%d failed: %s", attempt, max_retries, e)
            if attempt < max_retries:
                await asyncio.sleep(3)

    logger.error("MongoDB unavailable - starting in degraded mode (DB features will not work)")
    logger.error("   Set MONGO_URL to a valid MongoDB Atlas connection string in your Space secrets")
    _db_connected = False


async def disconnect_db() -> None:
    """Close the Motor client."""
    global _client, _db, _db_connected
    if _client:
        _client.close()
        _client = None
        _db = None
        _db_connected = False
        logger.info("MongoDB disconnected")


def get_db() -> AsyncIOMotorDatabase:
    if _db is None:
        raise RuntimeError("Database not initialised. Call connect_db() first.")
    return _db


def get_collection(name: str):
    return get_db()[name]


def is_db_connected() -> bool:
    return _db_connected


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
