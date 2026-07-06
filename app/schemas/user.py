"""User-related Pydantic schemas."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: EmailStr
    display_name: str = Field(..., min_length=1, max_length=100)
    password: str | None = None


class UserResponse(BaseModel):
    """Schema for user data in API responses."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    display_name: str
    avatar_url: str | None = None
    auth_provider: str
    reputation_score: int
    created_at: datetime
    home_zone_id: UUID | None = None


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    display_name: str | None = Field(None, min_length=1, max_length=100)
    avatar_url: str | None = None
    home_zone_id: UUID | None = None
    preferences: dict | None = None


class GoogleAuthRequest(BaseModel):
    """Schema for Google OAuth authentication."""
    token: str


class AuthResponse(BaseModel):
    """Schema for authentication response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
