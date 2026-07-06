"""FastAPI dependencies for route injection."""
from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

# Re-export core dependencies for convenient import from api.deps
from app.core.database import get_db
from app.core.redis import get_redis
from app.core.security import get_current_user, get_current_user_optional


class CommonQueryParams(BaseModel):
    """Common query parameters for list endpoints."""
    city_id: UUID | None = Field(default=None, description="Filter by city ID")
    zone_id: UUID | None = Field(default=None, description="Filter by zone ID")
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")

    @property
    def offset(self) -> int:
        """Calculate the database offset from page and page_size."""
        return (self.page - 1) * self.page_size


class GeoQueryParams(BaseModel):
    """Geospatial query parameters for location-based endpoints."""
    lat: float | None = Field(default=None, ge=-90, le=90, description="Latitude")
    lon: float | None = Field(default=None, ge=-180, le=180, description="Longitude")
    radius_km: float = Field(default=5.0, gt=0, le=50, description="Search radius in kilometers")

    @property
    def radius_meters(self) -> float:
        """Convert radius from kilometers to meters."""
        return self.radius_km * 1000
