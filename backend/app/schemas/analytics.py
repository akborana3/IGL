"""Pydantic schemas for analytics."""

from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel


class AnalyticsSummary(BaseModel):
    total_media: int
    total_views: int
    total_downloads: int
    featured_count: int
    categories_count: int


class DailyAnalytics(BaseModel):
    date: datetime
    total_views: int
    total_downloads: int


class AnalyticsResponse(BaseModel):
    summary: AnalyticsSummary
    daily: List[DailyAnalytics] = []
    top_media: List[dict] = []
