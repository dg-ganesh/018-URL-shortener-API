"""
Project : URL Shortener API

Project ID : 018

URL Repository
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.url_model import URL


class URLRepository:
    """Provide database operations for URL records."""

    def __init__(self, session: Session) -> None:
        """Initialize the repository with the database session."""
        self._session = session

    def create(self, url: URL) -> URL:
        """
        Persist a new URL record and return the refreshed entity.
        """
        self._session.add(url)
        self._session.commit()
        self._session.refresh(url)

        return url

    def get_by_id(self, url_id: int) -> URL | None:
        """Return a URL record by its database ID."""
        statement = select(URL).where(URL.id == url_id)

        return self._session.scalar(statement)

    def get_by_short_code(
        self,
        short_code: str,
    ) -> URL | None:
        """Return a URL record by its unique short code."""
        statement = select(URL).where(
            URL.short_code == short_code
        )

        return self._session.scalar(statement)

    def get_by_custom_alias(
        self,
        custom_alias: str,
    ) -> URL | None:
        """Return a URL record by its custom alias."""
        statement = select(URL).where(
            URL.custom_alias == custom_alias
        )

        return self._session.scalar(statement)

    def get_by_identifier(
        self,
        identifier: str,
    ) -> URL | None:
        """
        Return a URL record using either its short code
        or custom alias.
        """

        url = self.get_by_short_code(identifier)

        if url is not None:
            return url

        return self.get_by_custom_alias(identifier)

    def exists_by_short_code(
        self,
        short_code: str,
    ) -> bool:
        """Return whether a short code already exists."""
        statement = select(URL.id).where(
            URL.short_code == short_code
        )

        return self._session.scalar(statement) is not None

    def exists_by_custom_alias(
        self,
        custom_alias: str,
    ) -> bool:
        """Return whether a custom alias already exists."""
        statement = select(URL.id).where(
            URL.custom_alias == custom_alias
        )

        return self._session.scalar(statement) is not None

    def update(self, url: URL) -> URL:
        """
        Persist changes to an existing URL record.
        """
        self._session.add(url)
        self._session.commit()
        self._session.refresh(url)

        return url

    def delete(self, url: URL) -> URL:
        """
        Mark a URL as inactive rather than physically deleting it.

        Historical URL records are retained for future analytics.
        """
        url.is_active = False

        return self.update(url)