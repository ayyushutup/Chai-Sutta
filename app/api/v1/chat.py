"""Ask Tapri chat routes: AI-powered city assistant."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_current_user_optional, get_db

router = APIRouter()


# ── Schemas ─────────────────────────────────────────────────────────────────


class ChatRequest(BaseModel):
    """Chat message request."""
    message: str = Field(min_length=1, max_length=2000)
    city_id: UUID | None = None
    context: dict | None = None  # Additional context (location, etc.)


class ChatResponse(BaseModel):
    """Chat response from Tapri AI."""
    id: UUID | None = None
    message: str
    sources: list[dict] | None = None  # Referenced data sources
    suggestions: list[str] | None = None  # Follow-up suggestions
    created_at: str | None = None

    model_config = {"from_attributes": True}


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.post(
    "/",
    response_model=ChatResponse,
    summary="Ask Tapri a question",
)
async def ask_tapri(
    payload: ChatRequest,
    current_user=Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Ask the Tapri AI assistant a question about the city.

    Authentication is optional — anonymous users get limited responses.
    """
    # TODO: Implement chat service with LLM integration
    raise NotImplementedError("Chat service not yet implemented.")


@router.get(
    "/history",
    response_model=list[ChatResponse],
    summary="Get chat history",
)
async def get_chat_history(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get the authenticated user's chat history."""
    # TODO: Implement chat history service
    return []
