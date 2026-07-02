"""Application configuration loaded from environment variables."""

from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration. All values come from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Telegram
    api_id: int = 0
    api_hash: str = ""
    session_string: str = ""
    channel_id: int = 0

    # MongoDB
    mongo_url: str = "mongodb://localhost:27017"
    mongo_db: str = "ott_platform"

    # Admin / JWT
    admin_username: str = "admin"
    admin_password_hash: str = ""
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 1440

    # CORS
    cors_origins: str = "http://localhost:3000"

    # Sync
    sync_interval_seconds: int = 300

    # Streaming — tuned for performance
    chunk_size: int = 1048576  # 1 MB chunks (larger = fewer Telegram round trips)
    stream_buffer_size: int = 2097152  # 2 MB internal buffer for FFmpeg pipe
    max_concurrent_streams: int = 10  # max simultaneous stream connections

    # FFmpeg — for MKV → fMP4 remux
    ffmpeg_path: str = "ffmpeg"
    ffmpeg_buffer_size: str = "8192k"  # input buffer size for FFmpeg

    # Message cache — avoids redundant Telegram API calls during seeking
    message_cache_ttl: int = 120  # seconds before re-fetching message object

    # Storage (HF Bucket mount path for thumbnails)
    storage_path: str = "/data/thumbnails"
    storage_url: str = ""  # Public base URL for serving thumbnails (optional)

    @field_validator("cors_origins")
    @classmethod
    def parse_cors(cls, v: str) -> str:
        return v

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
