"""Common schemas and enums used across the application."""
from __future__ import annotations

import math
from enum import Enum
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, computed_field

T = TypeVar("T")


class GeoPoint(BaseModel):
    """Geographic coordinate point."""
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")


class PaginationParams(BaseModel):
    """Pagination query parameters."""
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""
    items: list[T]
    total: int
    page: int
    page_size: int

    @computed_field
    @property
    def total_pages(self) -> int:
        """Calculate total pages from total items and page size."""
        return math.ceil(self.total / self.page_size) if self.page_size > 0 else 0


class CategoryEnum(str, Enum):
    """Content category enumeration."""
    TRAFFIC = "traffic"
    WEATHER = "weather"
    POLITICS = "politics"
    SPORTS = "sports"
    ENTERTAINMENT = "entertainment"
    FOOD = "food"
    EMERGENCY = "emergency"
    TRANSPORT = "transport"
    CRIME = "crime"
    COMMUNITY = "community"


class SeverityEnum(str, Enum):
    """Severity level enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TimePeriod(str, Enum):
    """Time period filter enumeration."""
    LAST_HOUR = "last_hour"
    LAST_6H = "last_6h"
    LAST_24H = "last_24h"
    LAST_7D = "last_7d"
    LAST_30D = "last_30d"


class MoodEnum(str, Enum):
    """City mood enumeration."""
    CHILL = "chill"
    ACTIVE = "active"
    BUSY = "busy"
    CHAOTIC = "chaotic"
    BUZZING = "buzzing"
