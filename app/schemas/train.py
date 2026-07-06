"""Train status Pydantic schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TrainResponse(BaseModel):
    """Schema for train status data in API responses."""
    model_config = ConfigDict(from_attributes=True)

    train_number: str | None = None
    train_name: str | None = None
    line_name: str
    status: str
    delay_minutes: int
    direction: str | None = None
    platform: str | None = None
    stations: dict | None = None
    recorded_at: datetime
