"""
Project : URL Shortener API

Project ID : 018

URL API Schemas
"""

from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field


class URLCreateRequest(BaseModel):
    """Request payload for creating a shortened URL."""

    original_url: AnyHttpUrl = Field(
        ...,
        description="The original URL that should be shortened.",
    )

    custom_alias: str | None = Field(
        default=None,
        description=(
            "Optional custom alias for the shortened URL."
        ),
    )

    expires_at: datetime | None = Field(
        default=None,
        description="Optional UTC expiration timestamp for the URL.",
    )


class URLCreateResponse(BaseModel):
    """Response returned after successfully creating a shortened URL."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ...,
        description="Unique database identifier for the shortened URL.",
    )

    original_url: AnyHttpUrl = Field(
        ...,
        description="The original destination URL.",
    )

    short_code: str = Field(
        ...,
        description="Unique generated short code.",
    )

    custom_alias: str | None = Field(
        default=None,
        description="Custom alias assigned to the shortened URL.",
    )

    short_url: str = Field(
        ...,
        description="Complete shortened URL.",
    )

    created_at: datetime = Field(
        ...,
        description="Timestamp when the URL was created.",
    )

    is_active: bool = Field(
        ...,
        description="Whether the shortened URL is currently active.",
    )

    expires_at: datetime | None = Field(
        default=None,
        description="Optional expiration timestamp.",
    )


class URLDetailResponse(URLCreateResponse):
    """Detailed representation of a shortened URL."""


class URLLifecycleResponse(BaseModel):
    """Response returned after an URL lifecycle operation."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ...,
        description="Unique database identifier for the URL.",
    )

    short_code: str = Field(
        ...,
        description="Unique short code.",
    )

    is_active: bool = Field(
        ...,
        description="Current activation state of the URL.",
    )

    expires_at: datetime | None = Field(
        default=None,
        description="Optional expiration timestamp.",
    )