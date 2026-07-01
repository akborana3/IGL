"""Telethon client manager — connect, disconnect, and channel access."""

from __future__ import annotations

import logging
from typing import Optional

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import Channel

from app.core.config import settings

logger = logging.getLogger(__name__)

_client: Optional[TelegramClient] = None
_channel: Optional[Channel] = None


async def connect_telethon() -> None:
    """Create and connect the Telethon client using a string session."""
    global _client, _channel

    if not settings.session_string:
        logger.warning("No SESSION_STRING provided — Telegram features disabled")
        return

    _client = TelegramClient(
        session=StringSession(settings.session_string),
        api_id=settings.api_id,
        api_hash=settings.api_hash,
    )
    await _client.connect()

    if not await _client.is_user_authorized():
        logger.error("Telethon session is not authorized")
        raise RuntimeError("Telethon session not authorized")

    _channel = await _client.get_entity(settings.channel_id)
    logger.info("Telethon connected, channel resolved: %s", settings.channel_id)


async def disconnect_telethon() -> None:
    """Disconnect the Telethon client."""
    global _client, _channel
    if _client:
        await _client.disconnect()
        _client = None
        _channel = None
        logger.info("Telethon disconnected")


def get_client() -> TelegramClient:
    if _client is None:
        raise RuntimeError("Telethon client not initialised. Call connect_telethon() first.")
    return _client


def get_channel() -> Channel:
    if _channel is None:
        raise RuntimeError("Channel not resolved. Call connect_telethon() first.")
    return _channel


def is_connected() -> bool:
    return _client is not None and _client.is_connected()
