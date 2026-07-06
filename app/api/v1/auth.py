"""Authentication routes: registration, login, Google OAuth, and user info."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db

router = APIRouter()


# ── Request / Response Schemas ──────────────────────────────────────────────


class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    display_name: str = Field(min_length=2, max_length=100)
    city_id: UUID | None = None


class GoogleAuthRequest(BaseModel):
    """Schema for Google OAuth authentication."""
    id_token: str


class UserResponse(BaseModel):
    """Public user representation."""
    id: UUID
    email: str
    display_name: str
    avatar_url: str | None = None
    city_id: UUID | None = None
    is_active: bool = True

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    """Authentication response with JWT token."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Register a new user with email and password."""
    # TODO: Implement user creation service
    raise NotImplementedError("User registration not yet implemented.")


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Login with email and password",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Authenticate user with email/password and return JWT."""
    # TODO: Implement login service
    raise NotImplementedError("Login not yet implemented.")


@router.post(
    "/google",
    response_model=AuthResponse,
    summary="Authenticate with Google OAuth",
)
async def google_auth(
    payload: GoogleAuthRequest,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Authenticate or register a user via Google ID token."""
    # TODO: Implement Google OAuth flow
    raise NotImplementedError("Google auth not yet implemented.")


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user info",
)
async def get_me(
    current_user=Depends(get_current_user),
) -> Any:
    """Return the currently authenticated user's profile."""
    return current_user
