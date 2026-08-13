"""
Project : URL Shortener API

Project ID : 018

URL Redirect Business Logic
"""

from src.core.url.click_recorder import ClickRecorder
from src.core.url.url_lifecycle import (
    URLLifecycle,
    URLNotFoundError,
)
from src.models.url_model import URL
from src.services.click_repository import ClickRepository
from src.services.url_repository import URLRepository


class URLNotRedirectableError(Exception):
    """Raised when a URL cannot currently be redirected."""


class URLRedirector:
    """Resolve public URL identifiers and determine destinations."""

    def __init__(
        self,
        repository: URLRepository,
        click_repository: ClickRepository,
    ) -> None:
        """Initialize the redirect service."""
        self._repository = repository
        self._lifecycle = URLLifecycle(repository)
        self._click_recorder = ClickRecorder(click_repository)

    def resolve(self, identifier: str) -> URL:
        """
        Resolve a custom alias or short code to an active URL.

        Raises:
            URLNotFoundError:
                When the identifier does not exist.

            URLNotRedirectableError:
                When the URL is inactive or expired.
        """
        url = self._repository.get_by_custom_alias(
            identifier
        )

        if url is None:
            url = self._repository.get_by_short_code(
                identifier
            )

        if url is None:
            raise URLNotFoundError(
                f"URL identifier '{identifier}' was not found."
            )

        if not self._lifecycle.is_redirectable(url):
            raise URLNotRedirectableError(
                f"URL identifier '{identifier}' is not currently "
                "redirectable."
            )

        return url

    def get_destination(self, identifier: str) -> str:
        """
        Record a successful click and return the original destination.

        A click is recorded only after the identifier has been
        successfully resolved to an active, non-expired URL.
        """
        url = self.resolve(identifier)

        self._click_recorder.record(url.id)

        return str(url.original_url)