"""FastAPI application entry point — optimised for fast startup."""

from __future__ import annotations

import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.admin import router as admin_router
from app.api.home import router as home_router
from app.api.media import router as media_router
from app.api.search import router as search_router
from app.api.stream import router as stream_router
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.database.connection import connect_db, disconnect_db, is_db_connected
from app.telethon_exec.client import connect_telethon, disconnect_telethon
from app.telethon_exec.indexer import initial_scan
from app.workers.analytics_worker import start_analytics_worker, stop_analytics_worker
from app.workers.sync_worker import start_sync_worker, stop_sync_worker

setup_logging()
logger = logging.getLogger(__name__)

PORT = int(os.environ.get("PORT", 7860))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — parallel startup for faster boot."""
    logger.info("=" * 60)
    logger.info("Starting OTT Streaming Platform backend...")
    logger.info("  Port: %d", PORT)
    logger.info("  CORS Origins: %s", settings.cors_origins)
    logger.info("=" * 60)

    # --- Parallel init: MongoDB + Telegram at the same time ---
    db_task = asyncio.create_task(connect_db())
    tg_task = asyncio.create_task(_connect_telethon_safe())

    await asyncio.gather(db_task, tg_task)
    db_ok = is_db_connected()

    if db_ok:
        # Start background workers immediately
        start_sync_worker()
        start_analytics_worker()

        # Run initial scan in background (non-blocking — server is ready now)
        if tg_task.result():
            asyncio.create_task(_background_scan())
    else:
        logger.warning("Skipping Telegram sync — MongoDB not available")

    logger.info("=" * 60)
    logger.info("Backend is LIVE on port %d", PORT)
    logger.info("  Docs: http://0.0.0.0:%d/docs", PORT)
    logger.info("  Health: http://0.0.0.0:%d/health", PORT)
    logger.info("=" * 60)
    yield

    # Shutdown
    logger.info("Shutting down backend...")
    await stop_sync_worker()
    await stop_analytics_worker()
    await disconnect_telethon()
    await disconnect_db()
    logger.info("Backend shutdown complete")


async def _connect_telethon_safe() -> bool:
    """Connect to Telegram, return True on success."""
    try:
        await connect_telethon()
        return True
    except Exception as e:
        logger.error("Telegram connection failed: %s — running in degraded mode", e)
        return False


async def _background_scan() -> None:
    """Run initial scan in background (non-blocking)."""
    try:
        logger.info("Running initial scan (background)...")
        count = await initial_scan()
        logger.info("Initial scan complete: %d items indexed", count)
    except Exception as e:
        logger.error("Initial scan error: %s", e)


app = FastAPI(
    title="Premium OTT Streaming Platform",
    description="FastAPI backend for premium OTT streaming with Telegram media storage",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(home_router)
app.include_router(media_router)
app.include_router(search_router)
app.include_router(stream_router)
app.include_router(admin_router)


@app.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "ott-streaming-backend",
        "port": PORT,
        "db_connected": is_db_connected(),
    }


@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {
        "service": "Premium OTT Streaming Platform",
        "version": "1.0.0",
        "status": "running",
        "port": PORT,
        "docs": "/docs",
        "health": "/health",
        "db_connected": is_db_connected(),
    }
