"""JWT authentication, password hashing, and Google OAuth verification."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

import httpx
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.database import get_db
from app.core.exceptions import UnauthorizedException

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    auto_error=False,
)


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """Create a JWT access token.

    Args:
        data: Payload data (must include 'sub' for user identifier).
        expires_delta: Custom expiration time. Defaults to JWT_ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        Encoded JWT string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def verify_token(token: str) -> dict[str, Any] | None:
    """Verify and decode a JWT token.

    Returns:
        Decoded payload dict, or None if verification fails.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except jwt.PyJWTError:
        return None


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """FastAPI dependency: extract and validate the current authenticated user.

    Raises UnauthorizedException if the token is missing, invalid, or the user doesn't exist.
    """
    if token is None:
        raise UnauthorizedException("Authentication required.")

    payload = verify_token(token)
    if payload is None:
        raise UnauthorizedException("Invalid or expired token.")

    user_id = payload.get("sub")
    if user_id is None:
        raise UnauthorizedException("Invalid token payload.")

    # Lazy import to avoid circular dependency
    from app.models.user import User

    result = await db.execute(select(User).where(User.id == UUID(user_id)))
    user = result.scalar_one_or_none()

    if user is None:
        raise UnauthorizedException("User not found.")

    if not user.is_active:
        raise UnauthorizedException("User account is deactivated.")

    return user


async def get_current_user_optional(
    token: str | None = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Any | None:
    """FastAPI dependency: optionally extract the current user.

    Returns None instead of raising if not authenticated.
    """
    if token is None:
        return None

    payload = verify_token(token)
    if payload is None:
        return None

    user_id = payload.get("sub")
    if user_id is None:
        return None

    from app.models.user import User

    result = await db.execute(select(User).where(User.id == UUID(user_id)))
    user = result.scalar_one_or_none()

    if user is None or not user.is_active:
        return None

    return user


async def verify_google_token(token: str) -> dict[str, Any]:
    """Verify a Google OAuth ID token by calling Google's tokeninfo endpoint.

    Args:
        token: The Google ID token to verify.

    Returns:
        Dict with user info (email, name, picture, sub).

    Raises:
        UnauthorizedException: If the token is invalid or verification fails.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
        )

    if response.status_code != 200:
        raise UnauthorizedException("Invalid Google token.")

    data = response.json()

    # Verify the token was issued for our app
    if data.get("aud") != settings.GOOGLE_CLIENT_ID:
        raise UnauthorizedException("Google token audience mismatch.")

    return {
        "google_id": data.get("sub"),
        "email": data.get("email"),
        "name": data.get("name"),
        "picture": data.get("picture"),
        "email_verified": data.get("email_verified", "false") == "true",
    }
