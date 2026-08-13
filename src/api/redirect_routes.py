"""
Project : URL Shortener API

Project ID : 018

Public Redirect Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.core.url.url_lifecycle import URLNotFoundError
from src.core.url.url_redirector import (
    URLNotRedirectableError,
    URLRedirector,
)
from src.services.click_repository import ClickRepository
from src.services.database_service import get_database_session
from src.services.url_repository import URLRepository


router = APIRouter(
    tags=["Redirect"],
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


def get_url_redirector(
    repository: URLRepository = Depends(get_url_repository),
    click_repository: ClickRepository = Depends(
        get_click_repository
    ),
) -> URLRedirector:
    """Create the URL redirect service for the current request."""
    return URLRedirector(
        repository=repository,
        click_repository=click_repository,
    )


@router.get(
    "/{identifier}",
    include_in_schema=True,
)
def redirect_short_url(
    identifier: str,
    redirector: URLRedirector = Depends(get_url_redirector),
) -> RedirectResponse:
    """Redirect a short code or custom alias to its destination."""
    try:
        destination = redirector.get_destination(identifier)

    except URLNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except URLNotRedirectableError as exc:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail=str(exc),
        ) from exc

    return RedirectResponse(
        url=destination,
        status_code=status.HTTP_302_FOUND,
    )