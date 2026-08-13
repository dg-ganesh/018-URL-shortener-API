"""
Project : URL Shortener API

Project ID : 018

URL Creator
"""

from datetime import datetime

from pydantic import AnyHttpUrl

from src.config import Settings
from src.core.url.alias_validator import (
    AliasValidator,
    InvalidAliasError,
)
from src.core.url.short_code_generator import ShortCodeGenerator
from src.models.url_model import URL
from src.models.url_schema import URLCreateResponse
from src.services.url_repository import URLRepository


class URLCreationError(Exception):
    """Base exception for URL creation failures."""


class ShortCodeGenerationError(URLCreationError):
    """Raised when a unique short code cannot be generated."""


class AliasAlreadyExistsError(URLCreationError):
    """Raised when a custom alias is already in use."""


class URLCreator:
    """Handle the business workflow for creating shortened URLs."""

    def __init__(
        self,
        repository: URLRepository,
        settings: Settings,
        short_code_generator: ShortCodeGenerator | None = None,
        alias_validator: AliasValidator | None = None,
    ) -> None:
        """Initialize the URL creation service."""
        self._repository = repository
        self._settings = settings
        self._short_code_generator = (
            short_code_generator or ShortCodeGenerator()
        )
        self._alias_validator = (
            alias_validator or AliasValidator()
        )

    def create(
        self,
        original_url: AnyHttpUrl,
        expires_at: datetime | None = None,
        custom_alias: str | None = None,
    ) -> URLCreateResponse:
        """
        Create and persist a shortened URL.

        Args:
            original_url:
                The destination URL to shorten.

            expires_at:
                Optional expiration timestamp for the shortened URL.

            custom_alias:
                Optional custom public alias for the shortened URL.

        Raises:
            InvalidAliasError:
                If the supplied custom alias is invalid.

            AliasAlreadyExistsError:
                If the supplied custom alias is already in use.

            ShortCodeGenerationError:
                If a unique short code cannot be generated.
        """
        normalized_alias = self._validate_custom_alias(
            custom_alias
        )

        short_code = self._generate_unique_short_code()

        url = URL(
            original_url=str(original_url),
            short_code=short_code,
            custom_alias=normalized_alias,
            is_active=True,
            expires_at=expires_at,
        )

        saved_url = self._repository.create(url)

        public_identifier = (
            saved_url.custom_alias
            or saved_url.short_code
        )

        return URLCreateResponse(
            id=saved_url.id,
            original_url=saved_url.original_url,
            short_code=saved_url.short_code,
            custom_alias=saved_url.custom_alias,
            short_url=self._build_short_url(
                public_identifier
            ),
            created_at=saved_url.created_at,
            is_active=saved_url.is_active,
            expires_at=saved_url.expires_at,
        )

    def _validate_custom_alias(
        self,
        custom_alias: str | None,
    ) -> str | None:
        """Validate a custom alias and verify its uniqueness."""
        if custom_alias is None:
            return None

        normalized_alias = self._alias_validator.validate(
            custom_alias
        )

        if self._repository.exists_by_custom_alias(
            normalized_alias
        ):
            raise AliasAlreadyExistsError(
                f"Custom alias '{normalized_alias}' "
                "is already in use."
            )

        return normalized_alias

    def _generate_unique_short_code(self) -> str:
        """Generate a short code that does not already exist."""
        max_attempts = 10

        for _ in range(max_attempts):
            short_code = self._short_code_generator.generate()

            if not self._repository.exists_by_short_code(
                short_code
            ):
                return short_code

        raise ShortCodeGenerationError(
            "Unable to generate a unique short code."
        )

    def _build_short_url(
        self,
        public_identifier: str,
    ) -> str:
        """Build the complete public short URL."""
        return (
            f"{self._settings.base_url.rstrip('/')}"
            f"/{public_identifier}"
        )