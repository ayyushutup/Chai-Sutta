"""PostGIS helper functions for geospatial queries."""
from __future__ import annotations

from geoalchemy2 import WKTElement
from geoalchemy2.functions import ST_Contains, ST_DWithin, ST_Distance
from sqlalchemy import func


def point_from_coords(lat: float, lon: float) -> WKTElement:
    """Create a PostGIS POINT geometry from latitude and longitude.

    Note: WKT format is POINT(longitude latitude).

    Args:
        lat: Latitude coordinate.
        lon: Longitude coordinate.

    Returns:
        WKTElement with SRID 4326 (WGS 84).
    """
    return WKTElement(f"POINT({lon} {lat})", srid=4326)


def nearby_filter(
    geom_column, lat: float, lon: float, radius_meters: float
):
    """Create a spatial filter for finding geometries within a radius.

    Uses ST_DWithin for efficient index-backed distance queries.
    Casts to geography for accurate meter-based distances on the Earth's surface.

    Args:
        geom_column: SQLAlchemy column with geometry type.
        lat: Center latitude.
        lon: Center longitude.
        radius_meters: Search radius in meters.

    Returns:
        SQLAlchemy filter expression.
    """
    point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
    return ST_DWithin(
        func.cast(geom_column, func.Geography),
        func.cast(point, func.Geography),
        radius_meters,
    )


def distance_meters(geom_column, lat: float, lon: float):
    """Calculate distance in meters between a geometry column and a point.

    Uses geography cast for accurate Earth-surface distances.

    Args:
        geom_column: SQLAlchemy column with geometry type.
        lat: Target latitude.
        lon: Target longitude.

    Returns:
        SQLAlchemy expression for distance in meters.
    """
    point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
    return ST_Distance(
        func.cast(geom_column, func.Geography),
        func.cast(point, func.Geography),
    )


def area_contains(boundary_column, lat: float, lon: float):
    """Check if a boundary polygon contains a given point.

    Args:
        boundary_column: SQLAlchemy column with polygon geometry.
        lat: Point latitude.
        lon: Point longitude.

    Returns:
        SQLAlchemy filter expression (boolean).
    """
    point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
    return ST_Contains(boundary_column, point)
