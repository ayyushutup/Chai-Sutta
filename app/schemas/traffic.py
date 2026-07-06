"""Traffic-related Pydantic schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TrafficResponse(BaseModel):
    """Schema for individual traffic data point in API responses."""
    model_config = ConfigDict(from_attributes=True)

    road_name: str | None = None
    current_speed: float
    free_flow_speed: float
    congestion_level: str
    incidents: dict | None = None
    source: str
    recorded_at: datetime


class TrafficZoneResponse(BaseModel):
    """Schema for aggregated traffic data for a zone."""
    zone_name: str
    overall_congestion: str
    data_points: list[TrafficResponse]
