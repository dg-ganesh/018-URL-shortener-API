"""
Project : URL Shortener API

Project ID : 018

URL Click Repository
"""

from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.models.click_model import URLClick


class ClickRepository:
    """Provide database operations for URL click records."""

    def __init__(self, session: Session) -> None:
        """Initialize the repository with a database session."""
        self._session = session

    def create(self, url_id: int) -> URLClick:
        """Create and persist a click record for a URL."""
        click = URLClick(url_id=url_id)

        self._session.add(click)
        self._session.commit()
        self._session.refresh(click)

        return click

    def get_click_count(self, url_id: int) -> int:
        """Return the total number of clicks for a URL."""
        statement = select(
            func.count(URLClick.id)
        ).where(
            URLClick.url_id == url_id
        )

        return int(self._session.scalar(statement) or 0)

    def get_first_click_time(
        self,
        url_id: int,
    ) -> datetime | None:
        """Return the timestamp of the first recorded click."""
        statement = select(
            func.min(URLClick.clicked_at)
        ).where(
            URLClick.url_id == url_id
        )

        return self._session.scalar(statement)

    def get_last_click_time(
        self,
        url_id: int,
    ) -> datetime | None:
        """Return the timestamp of the most recent click."""
        statement = select(
            func.max(URLClick.clicked_at)
        ).where(
            URLClick.url_id == url_id
        )

        return self._session.scalar(statement)