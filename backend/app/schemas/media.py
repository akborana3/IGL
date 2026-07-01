"""Pydantic schemas for media endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class MediaBase(BaseModel):
    title: str
    description: str = ""
    caption: str = ""
    slug: str
    category: str = "Uncategorized"
    tags: List[str] = []
    duration: int = 0
    width: int = 0
    height: int = 0
    file_size: int = 0
    mime_type: str = ""
    thumbnail: Optional[str] = None
    featured: bool = False


class MediaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    telegram_message_id: int
    title: str
    slug: str
    category: str
    tags: List[str] = []
    duration: int = 0
    width: int = 0
    height: int = 0
    file_size: int = 0
    mime_type: str = ""
    thumbnail: Optional[str] = None
    upload_date: datetime
    views: int = 0
    downloads: int = 0
    featured: bool = False
    description: str = ""
    caption: str = ""


class MediaDetail(MediaResponse):
    channel_id: int = 0
    created_at: datetime
    updated_at: datetime


class MediaUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    caption: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    featured: Optional[bool] = None


class MediaFeatureUpdate(BaseModel):
    slug: str
    featured: bool
