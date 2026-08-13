"""
Project : URL Shortener API

Project ID : 018

URL API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.config import Settings, get_settings
from src.core.url.alias_validator import InvalidAliasError
from src.core.url.url_analytics import (
    URLAnalytics,
    URLAnalyticsError,
)
from src.core.url.url_creator import (
    AliasAlreadyExistsError,
    URLCreator,
)
from src.core.url.url_lifecycle import (
    URLAlreadyActiveError,
    URLAlreadyInactiveError,
    URLExpiredError,
    URLNotFoundError,
    URLLifecycle,
)
from src.models.analytics_schema import URLAnalyticsResponse
from src.models.url_schema import (
    URLCreateRequest,
    URLCreateResponse,
    URLDetailResponse,
    URLLifecycleResponse,
)
from src.services.click_repository import ClickRepository
from src.services.database_service import get_database_session
from src.services.url_repository import URLRepository


router = APIRouter(
    prefix="/api/v1",
    tags=["URLs"],
)


def get_url_repository(
    session: Session = Depends(get_database_session),
) -> URLRepository:
    """Create a URL repository for the current request."""
    return URLRepository(session)


def get_click_repository(
    session: Session = Depends(get_database_session),
) -> ClickRepository:
    """Create a click repository for the current request."""
    return ClickRepository(session)


def get_url_creator(
    repository: URLRepository = Depends(get_url_repository),
    settings: Settings = Depends(get_settings),
) -> URLCreator:
    """Create the URL creation service for the current request."""
    return URLCreator(
        repository=repository,
        settings=settings,
    )


def get_url_lifecycle(
    repository: URLRepository = Depends(get_url_repository),
) -> URLLifecycle:
    """Create the URL lifecycle service for the current request."""
    return URLLifecycle(repository)


def get_url_analytics_service(
    url_repository: URLRepository = Depends(
        get_url_repository
    ),
    click_repository: ClickRepository = Depends(
        get_click_repository
    ),
) -> URLAnalytics:
    """Create the URL analytics service for the current request."""
    return URLAnalytics(
        url_repository=url_repository,
        click_repository=click_repository,
    )


@router.post(
    "/urls",
    response_model=URLCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    request: URLCreateRequest,
    creator: URLCreator = Depends(get_url_creator),
) -> URLCreateResponse:
    """Create a new shortened URL."""
    try:
        return creator.create(
            original_url=request.original_url,
            expires_at=request.expires_at,
            custom_alias=request.custom_alias,
        )

    except InvalidAliasError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except AliasAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get(
    "/urls/{url_id}",
    response_model=URLDetailResponse,
)
def get_url(
    url_id: int,
    lifecycle: URLLifecycle = Depends(get_url_lifecycle),
    settings: Settings = Depends(get_settings),
) -> URLDetailResponse:
    """Return details for a shortened URL."""
    try:
        url = lifecycle.get_url(url_id)

    except URLNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    public_identifier = (
        url.custom_alias
        or url.short_code
    )

    short_url = (
        f"{settings.base_url.rstrip('/')}"
        f"/{public_identifier}"
    )

    return URLDetailResponse(
        id=url.id,
        original_url=url.original_url,
        short_code=url.short_code,
        custom_alias=url.custom_alias,
        short_url=short_url,
        created_at=url.created_at,
        is_active=url.is_active,
        expires_at=url.expires_at,
    )


@router.get(
    "/urls/{url_id}/analytics",
    response_model=URLAnalyticsResponse,
)
def get_url_analytics(
    url_id: int,
    analytics: URLAnalytics = Depends(
        get_url_analytics_service
    ),
) -> URLAnalyticsResponse:
    """Return click analytics for a shortened URL."""
    try:
        return analytics.get_analytics(url_id)

    except URLAnalyticsError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/analytics/{identifier}",
    response_model=URLAnalyticsResponse,
)
def get_analytics_by_identifier(
    identifier: str,
    url_repository: URLRepository = Depends(
        get_url_repository
    ),
    analytics: URLAnalytics = Depends(
        get_url_analytics_service
    ),
) -> URLAnalyticsResponse:
    """
    Return click analytics using a short code
    or custom alias.
    """

    url = url_repository.get_by_identifier(
        identifier
    )

    if url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Short URL '{identifier}' "
                "was not found."
            ),
        )

    try:
        return analytics.get_analytics(
            url.id
        )

    except URLAnalyticsError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/urls/{url_id}/activate",
    response_model=URLLifecycleResponse,
)
def activate_url(
    url_id: int,
    lifecycle: URLLifecycle = Depends(
        get_url_lifecycle
    ),
) -> URLLifecycleResponse:
    """Activate a shortened URL."""
    try:
        url = lifecycle.activate(url_id)

    except URLNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except URLAlreadyActiveError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    except URLExpiredError as exc:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail=str(exc),
        ) from exc

    return URLLifecycleResponse(
        id=url.id,
        short_code=url.short_code,
        is_active=url.is_active,
        expires_at=url.expires_at,
    )


@router.patch(
    "/urls/{url_id}/deactivate",
    response_model=URLLifecycleResponse,
)
def deactivate_url(
    url_id: int,
    lifecycle: URLLifecycle = Depends(
        get_url_lifecycle
    ),
) -> URLLifecycleResponse:
    """Deactivate a shortened URL."""
    try:
        url = lifecycle.deactivate(url_id)

    except URLNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except URLAlreadyInactiveError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return URLLifecycleResponse(
        id=url.id,
        short_code=url.short_code,
        is_active=url.is_active,
        expires_at=url.expires_at,
    )


@router.delete(
    "/urls/{url_id}",
    response_model=URLLifecycleResponse,
)
def delete_url(
    url_id: int,
    lifecycle: URLLifecycle = Depends(
        get_url_lifecycle
    ),
) -> URLLifecycleResponse:
    """Soft-delete a shortened URL."""
    try:
        url = lifecycle.delete(url_id)

    except URLNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return URLLifecycleResponse(
        id=url.id,
        short_code=url.short_code,
        is_active=url.is_active,
        expires_at=url.expires_at,
    )