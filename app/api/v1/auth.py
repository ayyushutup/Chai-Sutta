"""Authentication routes: registration, login, Google OAuth, and user profile retrieving."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.exceptions import BadRequestException
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
    verify_google_token,
)
from app.models.user import User
from app.schemas.user import AuthResponse, GoogleAuthRequest, UserCreate, UserResponse

router = APIRouter()


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
    # Check if user already exists
    existing_user_stmt = select(User).where(User.email == payload.email)
    existing_user_result = await db.execute(existing_user_stmt)
    if existing_user_result.scalar_one_or_none() is not None:
        raise BadRequestException("Email already registered.")

    # Create the new user
    if not payload.password:
        raise BadRequestException("Password is required for email registration.")

    hashed_pw = hash_password(payload.password)
    user = User(
        email=payload.email,
        display_name=payload.display_name,
        password_hash=hashed_pw,
        auth_provider="email",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Generate JWT
    access_token = create_access_token(data={"sub": str(user.id)})

    return AuthResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user),
    )


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
    # Retrieve user
    user_stmt = select(User).where(User.email == form_data.username)
    user_result = await db.execute(user_stmt)
    user = user_result.scalar_one_or_none()

    if user is None or user.auth_provider != "email" or not user.password_hash:
        raise BadRequestException("Incorrect email or password.")

    if not verify_password(form_data.password, user.password_hash):
        raise BadRequestException("Incorrect email or password.")

    if not user.is_active:
        raise BadRequestException("User account is deactivated.")

    # Generate JWT
    access_token = create_access_token(data={"sub": str(user.id)})

    return AuthResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user),
    )


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
    # Verify the Google ID token
    google_payload = await verify_google_token(payload.token)

    # Check if user exists by email
    user_stmt = select(User).where(User.email == google_payload["email"])
    user_result = await db.execute(user_stmt)
    user = user_result.scalar_one_or_none()

    if user is None:
        # Register new Google user
        user = User(
            email=google_payload["email"],
            display_name=google_payload["name"],
            avatar_url=google_payload["picture"],
            auth_provider="google",
            auth_provider_id=google_payload["google_id"],
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    else:
        # If user exists but is not Google auth_provider, update it or allow login
        if user.auth_provider != "google":
            user.auth_provider = "google"
            user.auth_provider_id = google_payload["google_id"]
            if google_payload["picture"] and not user.avatar_url:
                user.avatar_url = google_payload["picture"]
            db.add(user)
            await db.commit()
            await db.refresh(user)

    if not user.is_active:
        raise BadRequestException("User account is deactivated.")

    # Generate JWT
    access_token = create_access_token(data={"sub": str(user.id)})

    return AuthResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user),
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user info",
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    """Return the currently authenticated user's profile."""
    return UserResponse.model_validate(current_user)
