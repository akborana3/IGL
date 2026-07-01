"""Pydantic schemas for admin authentication."""

from __future__ import annotations

from pydantic import BaseModel


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str


class AdminDashboardResponse(BaseModel):
    total_media: int
    total_views: int
    total_downloads: int
    last_sync: str = ""
    sync_status: str = "idle"
