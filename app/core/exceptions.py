"""Custom exception classes and FastAPI exception handlers."""
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ChaiSuttaException(Exception):
    """Base exception for the Chai Sutta application."""

    def __init__(
        self,
        detail: str = "An unexpected error occurred.",
        status_code: int = 500,
    ) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class NotFoundException(ChaiSuttaException):
    """Resource not found (404)."""

    def __init__(self, detail: str = "Resource not found.") -> None:
        super().__init__(detail=detail, status_code=404)


class UnauthorizedException(ChaiSuttaException):
    """Authentication required or failed (401)."""

    def __init__(self, detail: str = "Authentication required.") -> None:
        super().__init__(detail=detail, status_code=401)


class ForbiddenException(ChaiSuttaException):
    """Insufficient permissions (403)."""

    def __init__(self, detail: str = "Insufficient permissions.") -> None:
        super().__init__(detail=detail, status_code=403)


class BadRequestException(ChaiSuttaException):
    """Invalid request data (400)."""

    def __init__(self, detail: str = "Bad request.") -> None:
        super().__init__(detail=detail, status_code=400)


class RateLimitException(ChaiSuttaException):
    """Rate limit exceeded (429)."""

    def __init__(self, detail: str = "Rate limit exceeded. Please try again later.") -> None:
        super().__init__(detail=detail, status_code=429)


class ExternalServiceException(ChaiSuttaException):
    """External service call failed (502)."""

    def __init__(self, detail: str = "External service unavailable.") -> None:
        super().__init__(detail=detail, status_code=502)


def register_exception_handlers(app: FastAPI) -> None:
    """Register all custom exception handlers on the FastAPI application."""

    @app.exception_handler(ChaiSuttaException)
    async def chai_sutta_exception_handler(
        request: Request, exc: ChaiSuttaException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "detail": exc.detail,
                "status_code": exc.status_code,
            },
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(
        request: Request, exc: ValueError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "error": True,
                "detail": str(exc),
                "status_code": 400,
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "detail": "Internal server error.",
                "status_code": 500,
            },
        )
