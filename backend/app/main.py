"""FastAPI application entry point."""

from __future__ import annotations

import logging
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
from app.database.connection import connect_db, disconnect_db
from app.telethon_exec.client import connect_telethon, disconnect_telethon
from app.telethon_exec.indexer import initial_scan
from app.workers.analytics_worker import start_analytics_worker, stop_analytics_worker
from app.workers.sync_worker import start_sync_worker, stop_sync_worker

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    logger.info("Starting OTT Streaming Platform backend...")

    # Connect to MongoDB
    await connect_db()

    # Connect to Telegram
    try:
        await connect_telethon()
        # Run initial scan
        logger.info("Running initial scan...")
        count = await initial_scan()
        logger.info("Initial scan complete: %d items", count)
        # Start background workers
        start_sync_worker()
        start_analytics_worker()
    except Exception as e:
        logger.error("Telegram connection failed: %s — running in degraded mode", e)

    logger.info("Backend started successfully")
    yield

    # Shutdown
    logger.info("Shutting down backend...")
    await stop_sync_worker()
    await stop_analytics_worker()
    await disconnect_telethon()
    await disconnect_db()
    logger.info("Backend shutdown complete")


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
    return {"status": "ok", "service": "ott-streaming-backend"}


@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {
        "service": "Premium OTT Streaming Platform",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }
