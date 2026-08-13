"""
Project : URL Shortener API

Project ID : 018

URL Lifecycle Business Logic
"""

from datetime import datetime, timezone

from src.models.url_model import URL
from src.services.url_repository import URLRepository


class URLLifecycleError(Exception):
    """Base exception for URL lifecycle operations."""


class URLNotFoundError(URLLifecycleError):
    """Raised when a requested URL does not exist."""


class URLAlreadyActiveError(URLLifecycleError):
    """Raised when activating an already active URL."""


class URLAlreadyInactiveError(URLLifecycleError):
    """Raised when deactivating an already inactive URL."""


class URLExpiredError(URLLifecycleError):
    """Raised when an expired URL cannot be activated."""


class URLLifecycle:
    """Manage the business lifecycle of shortened URLs."""

    def __init__(self, repository: URLRepository) -> None:
        """Initialize the lifecycle service."""
        self._repository = repository

    def get_url(self, url_id: int) -> URL:
        """Retrieve a URL or raise an error when it does not exist."""
        url = self._repository.get_by_id(url_id)

        if url is None:
            raise URLNotFoundError(
                f"URL with ID {url_id} was not found."
            )

        return url

    def activate(self, url_id: int) -> URL:
        """Activate an existing non-expired URL."""
        url = self.get_url(url_id)

        if url.is_active:
            raise URLAlreadyActiveError(
                f"URL with ID {url_id} is already active."
            )

        if self.is_expired(url):
            raise URLExpiredError(
                f"URL with ID {url_id} has expired."
            )

        url.is_active = True

        return self._repository.update(url)

    def deactivate(self, url_id: int) -> URL:
        """Deactivate an active URL."""
        url = self.get_url(url_id)

        if not url.is_active:
            raise URLAlreadyInactiveError(
                f"URL with ID {url_id} is already inactive."
            )

        url.is_active = False

        return self._repository.update(url)

    def delete(self, url_id: int) -> URL:
        """
        Soft-delete a URL by marking it inactive.
        """
        url = self.get_url(url_id)

        url.is_active = False

        return self._repository.update(url)

    def is_expired(self, url: URL) -> bool:
        """Return whether a URL has passed its expiration time."""
        if url.expires_at is None:
            return False

        current_time = datetime.now(timezone.utc)

        expiration_time = url.expires_at

        if expiration_time.tzinfo is None:
            expiration_time = expiration_time.replace(
                tzinfo=timezone.utc
            )

        return expiration_time <= current_time

    def is_redirectable(self, url: URL) -> bool:
        """
        Return whether a URL is currently eligible for redirection.
        """
        if not url.is_active:
            return False

        if self.is_expired(url):
            return False

        return True