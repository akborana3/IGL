"""Background sync worker — continuously checks for new Telegram messages."""

from __future__ import annotations

import asyncio
import logging

from app.core.config import settings
from app.telethon_exec.indexer import sync_new_messages

logger = logging.getLogger(__name__)

_sync_task: asyncio.Task | None = None
_stop_event = asyncio.Event()


async def _sync_loop() -> None:
    """Run sync_new_messages on a configured interval."""
    logger.info("Sync worker started (interval=%ds)", settings.sync_interval_seconds)
    while not _stop_event.is_set():
        try:
            count = await sync_new_messages()
            if count > 0:
                logger.info("Sync worker: %d new items indexed", count)
        except Exception as e:
            logger.error("Sync worker error: %s", e)

        try:
            await asyncio.wait_for(_stop_event.wait(), timeout=settings.sync_interval_seconds)
        except asyncio.TimeoutError:
            pass  # Normal: timeout means interval elapsed, continue loop

    logger.info("Sync worker stopped")


def start_sync_worker() -> None:
    """Start the background sync task."""
    global _sync_task, _stop_event
    _stop_event = asyncio.Event()
    _sync_task = asyncio.create_task(_sync_loop())


async def stop_sync_worker() -> None:
    """Stop the background sync task."""
    global _sync_task
    _stop_event.set()
    if _sync_task:
        await _sync_task
        _sync_task = None
    logger.info("Sync worker stopped")