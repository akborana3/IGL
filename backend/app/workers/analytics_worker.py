"""Background analytics worker — aggregation, cleanup, health monitoring."""

from __future__ import annotations

import asyncio
import logging
import os
import shutil
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

_task: asyncio.Task | None = None
_stop_event = asyncio.Event()

TEMP_DIR = "/tmp/ott_temp"


async def _analytics_loop() -> None:
    """Run periodic analytics aggregation and cleanup."""
    logger.info("Analytics worker started (interval=3600s)")
    while not _stop_event.is_set():
        try:
            # Clean up temporary files
            if os.path.exists(TEMP_DIR):
                for filename in os.listdir(TEMP_DIR):
                    filepath = os.path.join(TEMP_DIR, filename)
                    if os.path.isfile(filepath):
                        stat = os.stat(filepath)
                        # Remove files older than 1 hour
                        age = (datetime.now(timezone.utc).timestamp() - stat.st_mtime)
                        if age > 3600:
                            os.remove(filepath)
                            logger.debug("Cleaned up temp file: %s", filename)

        except Exception as e:
            logger.error("Analytics worker error: %s", e)

        try:
            await asyncio.wait_for(_stop_event.wait(), timeout=3600)
        except asyncio.TimeoutError:
            pass

    logger.info("Analytics worker stopped")


def start_analytics_worker() -> None:
    """Start the background analytics task."""
    global _task, _stop_event
    _stop_event = asyncio.Event()
    _task = asyncio.create_task(_analytics_loop())


async def stop_analytics_worker() -> None:
    """Stop the background analytics task."""
    global _task
    _stop_event.set()
    if _task:
        await _task
        _task = None
    logger.info("Analytics worker stopped")