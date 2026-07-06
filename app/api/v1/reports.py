"""Community reports routes: CRUD, voting, and nearby."""
from __future__ import annotations

from typing import Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db

router = APIRouter()


# ── Schemas ─────────────────────────────────────────────────────────────────


class ReportResponse(BaseModel):
    """Community report response."""
    id: UUID
    title: str
    description: str
    category: str  # pothole, water, power, traffic, safety, other
    city_id: UUID
    zone_id: UUID | None = None
    lat: float | None = None
    lon: float | None = None
    image_url: str | None = None
    upvotes: int = 0
    downvotes: int = 0
    status: str = "open"  # open, acknowledged, resolved
    created_by: UUID | None = None
    created_at: str | None = None

    model_config = {"from_attributes": True}


class PaginatedReportResponse(BaseModel):
    """Paginated report list."""
    items: list[ReportResponse]
    total: int
    page: int
    page_size: int
    has_next: bool


class VoteRequest(BaseModel):
    """Vote on a report."""
    vote_type: Literal["up", "down"]


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.get(
    "/",
    response_model=PaginatedReportResponse,
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
    # TODO: Implement reports listing service
    return PaginatedReportResponse(items=[], total=0, page=page, page_size=page_size, has_next=False)


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
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Create a community report with optional image upload."""
    # TODO: Implement report creation with file upload
    raise NotImplementedError("Report creation not yet implemented.")


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
    # TODO: Implement report detail service
    raise NotImplementedError("Report detail not yet implemented.")


@router.post(
    "/{report_id}/vote",
    summary="Vote on a report",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def vote_on_report(
    report_id: UUID,
    payload: VoteRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Upvote or downvote a community report."""
    # TODO: Implement voting service
    raise NotImplementedError("Voting not yet implemented.")


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
    """Get community reports near a geographic point."""
    # TODO: Implement nearby reports service
    return []
