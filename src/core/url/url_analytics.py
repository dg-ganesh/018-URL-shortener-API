"""
Project : URL Shortener API

Project ID : 018

URL Analytics Business Logic
"""

from src.models.url_schema import URLDetailResponse
from src.models.analytics_schema import URLAnalyticsResponse
from src.services.click_repository import ClickRepository
from src.services.url_repository import URLRepository


class URLAnalyticsError(Exception):
    """Base exception for URL analytics failures."""


class URLAnalytics:
    """Provide analytics for shortened URLs."""

    def __init__(
        self,
        url_repository: URLRepository,
        click_repository: ClickRepository,
    ) -> None:
        """Initialize the analytics service."""
        self._url_repository = url_repository
        self._click_repository = click_repository

    def get_analytics(
        self,
        url_id: int,
    ) -> URLAnalyticsResponse:
        """
        Return click analytics for a shortened URL.

        Raises:
            URLAnalyticsError:
                When the requested URL does not exist.
        """
        url = self._url_repository.get_by_id(url_id)

        if url is None:
            raise URLAnalyticsError(
                f"URL with ID '{url_id}' was not found."
            )

        total_clicks = self._click_repository.get_click_count(
            url_id
        )

        first_clicked_at = (
            self._click_repository.get_first_click_time(
                url_id
            )
        )

        last_clicked_at = (
            self._click_repository.get_last_click_time(
                url_id
            )
        )

        return URLAnalyticsResponse(
            url_id=url.id,
            short_code=url.short_code,
            total_clicks=total_clicks,
            first_clicked_at=first_clicked_at,
            last_clicked_at=last_clicked_at,
        )