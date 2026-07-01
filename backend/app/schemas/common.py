"""Common Pydantic schemas: pagination and generic response wrappers."""

from __future__ import annotations

from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationInfo(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    pagination: PaginationInfo


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = ""
    data: Optional[T] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    detail: Optional[str] = None
