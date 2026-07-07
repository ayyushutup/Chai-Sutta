"""Community report Pydantic schemas."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from typing import Any
from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.common import GeoPoint, SeverityEnum


class ReportCreate(BaseModel):
    """Schema for creating a new community report."""
    content: str = Field(..., min_length=1)
    category: str = Field(..., max_length=50)
    severity: SeverityEnum = SeverityEnum.LOW
    city_id: UUID
    location: GeoPoint | None = None
    media_type: str = "none"


class ReportResponse(BaseModel):
    """Schema for community report data in API responses."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    content: str
    category: str
    severity: str
    zone_id: UUID | None = None
    city_id: UUID
    upvotes: int
    downvotes: int
    verification_status: str
    ai_extracted_text: str | None = None
    media_type: str
    media_url: str | None = None
    created_at: datetime
    expires_at: datetime | None = None
    location: GeoPoint | None = None

    @model_validator(mode="before")
    @classmethod
    def parse_location(cls, data: Any) -> Any:
        if not isinstance(data, dict) and hasattr(data, "location"):
            lat, lon = None, None
            if data.location is not None:
                try:
                    wkb_val = data.location.data
                    if isinstance(wkb_val, str):
                        wkb_bytes = bytes.fromhex(wkb_val)
                    else:
                        wkb_bytes = bytes(wkb_val)
                    
                    import struct
                    byte_order = wkb_bytes[0]
                    fmt = "<" if byte_order == 1 else ">"
                    geom_type = struct.unpack(f"{fmt}I", wkb_bytes[1:5])[0]
                    has_srid = bool(geom_type & 0x20000000)
                    offset = 5
                    if has_srid:
                        offset += 4
                    # POINT geometry stores (longitude, latitude) as (x, y)
                    lon, lat = struct.unpack(f"{fmt}dd", wkb_bytes[offset:offset+16])
                except Exception as e:
                    import sys
                    print(f"ERROR PARSING BINARY WKB: {e}", file=sys.stderr)
            
            # Convert object attributes to dict
            data_dict = {}
            for field_name in cls.model_fields.keys():
                if field_name == "location":
                    data_dict["location"] = {"lat": lat, "lon": lon} if lat is not None else None
                elif hasattr(data, field_name):
                    data_dict[field_name] = getattr(data, field_name)
            return data_dict
        return data
