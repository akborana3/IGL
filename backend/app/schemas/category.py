"""Pydantic schemas for categories."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class CategoryResponse(BaseModel):
    id: str
    name: str
    slug: str
    icon: str = ""
    description: str = ""
    media_count: int = 0


class CategoryWithMedia(CategoryResponse):
    """Category response that includes a sample of media items."""
    pass
