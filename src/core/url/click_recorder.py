"""
Project : URL Shortener API

Project ID : 018

URL Click Recorder
"""

from src.models.click_model import URLClick
from src.services.click_repository import ClickRepository


class ClickRecordingError(Exception):
    """Base exception for click recording failures."""


class ClickRecorder:
    """Record successful URL clicks."""

    def __init__(
        self,
        repository: ClickRepository,
    ) -> None:
        """Initialize the click recorder."""
        self._repository = repository

    def record(self, url_id: int) -> URLClick:
        """
        Record a successful click for a URL.

        The caller is responsible for ensuring that the URL has
        already passed redirectability validation.
        """
        try:
            return self._repository.create(url_id)

        except Exception as exc:
            raise ClickRecordingError(
                f"Unable to record click for URL {url_id}."
            ) from exc