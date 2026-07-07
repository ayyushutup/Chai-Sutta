"""Community reports routes: CRUD, voting, and nearby."""
from __future__ import annotations

import os
import uuid
from typing import Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.exceptions import BadRequestException, NotFoundException
from app.core.geo import point_from_coords, nearby_filter
from app.models.report import CommunityReport
from app.models.user import User
from app.schemas.common import PaginatedResponse
from app.schemas.report import ReportResponse

from pydantic import BaseModel

router = APIRouter()


class VoteRequest(BaseModel):
    """Vote on a report."""
    vote_type: Literal["up", "down"]


@router.get(
    "/",
    response_model=PaginatedResponse[ReportResponse],
    summary="List community reports",
)
async def list_reports(
    city_id: UUID | None = Query(default=None),
    zone_id: UUID | None = Query(default=None),
    category: str | None = Query(default=None),
    report_status: str | None = Query(default=None, alias="status"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """List community reports with optional filters and pagination."""
    stmt = select(CommunityReport).where(CommunityReport.is_active == True)

    if city_id:
        stmt = stmt.where(CommunityReport.city_id == city_id)
    if zone_id:
        stmt = stmt.where(CommunityReport.zone_id == zone_id)
    if category:
        stmt = stmt.where(CommunityReport.category == category)
    if report_status:
        stmt = stmt.where(CommunityReport.verification_status == report_status)

    # Order by newest
    stmt = stmt.order_by(CommunityReport.created_at.desc())

    # Get total count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    # Pagination
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    reports = result.scalars().all()

    items = [ReportResponse.model_validate(r) for r in reports]

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post(
    "/",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a community report",
)
async def create_report(
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    city_id: UUID = Form(...),
    zone_id: UUID | None = Form(default=None),
    lat: float | None = Form(default=None),
    lon: float | None = Form(default=None),
    image: UploadFile | None = File(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Create a community report with optional image upload."""
    content = f"{title}: {description}" if title else description

    media_url = None
    media_type = "none"
    if image is not None and image.filename:
        os.makedirs("uploads", exist_ok=True)
        file_ext = os.path.splitext(image.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        filepath = os.path.join("uploads", unique_filename)
        with open(filepath, "wb") as buffer:
            buffer.write(await image.read())
        media_url = f"/uploads/{unique_filename}"
        media_type = "image"

    location = None
    if lat is not None and lon is not None:
        location = point_from_coords(lat, lon)

    report = CommunityReport(
        user_id=current_user.id,
        city_id=city_id,
        zone_id=zone_id,
        category=category,
        content=content,
        location=location,
        media_type=media_type,
        media_url=media_url,
        verification_status="unverified",
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)

    return ReportResponse.model_validate(report)


@router.get(
    "/nearby",
    response_model=list[ReportResponse],
    summary="Get reports near a point",
)
async def get_nearby_reports(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(default=5.0, gt=0, le=50),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get community reports near a geographic point, sorted by proximity."""
    radius_meters = radius_km * 1000.0

    from geoalchemy2 import Geography
    point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)

    stmt = select(CommunityReport).where(
        and_(
            CommunityReport.is_active == True,
            func.ST_DWithin(
                func.cast(CommunityReport.location, Geography),
                func.cast(point, Geography),
                radius_meters,
            )
        )
    )

    # Sort by distance
    stmt = stmt.order_by(
        func.ST_Distance(
            func.cast(CommunityReport.location, Geography),
            func.cast(point, Geography),
        )
    )

    result = await db.execute(stmt)
    reports = result.scalars().all()

    return [ReportResponse.model_validate(r) for r in reports]


@router.get(
    "/{report_id}",
    response_model=ReportResponse,
    summary="Get a report",
)
async def get_report(
    report_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get a single community report by ID."""
    stmt = select(CommunityReport).where(
        and_(
            CommunityReport.id == report_id,
            CommunityReport.is_active == True
        )
    )
    result = await db.execute(stmt)
    report = result.scalar_one_or_none()

    if report is None:
        raise NotFoundException("Report not found.")

    return ReportResponse.model_validate(report)


@router.post(
    "/{report_id}/vote",
    summary="Vote on a report",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def vote_on_report(
    report_id: UUID,
    payload: VoteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Upvote or downvote a community report."""
    stmt = select(CommunityReport).where(
        and_(
            CommunityReport.id == report_id,
            CommunityReport.is_active == True
        )
    )
    result = await db.execute(stmt)
    report = result.scalar_one_or_none()

    if report is None:
        raise NotFoundException("Report not found.")

    if payload.vote_type == "up":
        report.upvotes += 1
    elif payload.vote_type == "down":
        report.downvotes += 1

    db.add(report)
    await db.commit()
