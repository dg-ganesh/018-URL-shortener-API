"""
Project : URL Shortener API

Project ID : 018

Health API Routes
"""

from fastapi import APIRouter


router = APIRouter(
    tags=["Health"],
)


@router.get(
    "/health",
    summary="Health check",
)
def health_check() -> dict[str, str]:
    """
    Return the current application health status.
    """
    return {"status": "healthy"}
