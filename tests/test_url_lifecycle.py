"""
Project : URL Shortener API

Project ID : 018

URL Lifecycle Tests
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

import pytest

from src.core.url.url_lifecycle import (
    URLAlreadyActiveError,
    URLAlreadyInactiveError,
    URLExpiredError,
    URLNotFoundError,
    URLLifecycle,
)
from src.models.url_model import URL


def create_url(
    *,
    is_active: bool = True,
    expires_at: datetime | None = None,
) -> URL:
    """Create an in-memory URL entity for testing."""
    return URL(
        id=1,
        original_url="https://www.example.com",
        short_code="abc123",
        is_active=is_active,
        expires_at=expires_at,
    )


def create_repository(url: URL | None) -> Mock:
    """Create a mocked URL repository."""
    repository = Mock()
    repository.get_by_id.return_value = url
    repository.update.side_effect = lambda value: value

    return repository


def test_get_url_returns_existing_url() -> None:
    """An existing URL should be returned successfully."""
    url = create_url()
    repository = create_repository(url)
    lifecycle = URLLifecycle(repository)

    result = lifecycle.get_url(1)

    assert result is url
    repository.get_by_id.assert_called_once_with(1)


def test_get_url_raises_when_url_does_not_exist() -> None:
    """A missing URL should raise URLNotFoundError."""
    repository = create_repository(None)
    lifecycle = URLLifecycle(repository)

    with pytest.raises(URLNotFoundError):
        lifecycle.get_url(999)


def test_active_url_is_not_expired() -> None:
    """A URL without an expiration timestamp should not expire."""
    url = create_url(expires_at=None)
    repository = create_repository(url)
    lifecycle = URLLifecycle(repository)

    assert lifecycle.is_expired(url) is False


def test_future_expiration_is_not_expired() -> None:
    """A URL with a future expiration should remain valid."""
    expiration = datetime.now(timezone.utc) + timedelta(hours=1)
    url = create_url(expires_at=expiration)
    repository = create_repository(url)
    lifecycle = URLLifecycle(repository)

    assert lifecycle.is_expired(url) is False


def test_past_expiration_is_expired() -> None:
    """A URL with a past expiration should be expired."""
    expiration = datetime.now(timezone.utc) - timedelta(hours=1)
    url = create_url(expires_at=expiration)
    repository = create_repository(url)
    lifecycle = URLLifecycle(repository)

    assert lifecycle.is_expired(url) is True


def test_active_non_expired_url_is_redirectable() -> None:
    """An active, non-expired URL should be redirectable."""
    expiration = datetime.now(timezone.utc) + timedelta(hours=1)
    url = create_url(
        is_active=True,
        expires_at=expiration,
    )
    repository = create_repository(url)
    lifecycle = URLLifecycle(repository)

    assert lifecycle.is_redirectable(url) is True


def test_inactive_url_is_not_redirectable() -> None:
    """An inactive URL should not be redirectable."""
    url = create_url(is_active=False)
    repository = create_repository(url)
    lifecycle = URLLifecycle(repository)

    assert lifecycle.is_redirectable(url) is False


def test_expired_url_is_not_redirectable() -> None:
    """An expired URL should not be redirectable."""
    expiration = datetime.now(timezone.utc) - timedelta(hours=1)
    url = create_url(expires_at=expiration)
    repository = create_repository(url)
    lifecycle = URLLifecycle(repository)

    assert lifecycle.is_redirectable(url) is False


def test_deactivate_active_url() -> None:
    """An active URL should become inactive."""
    url = create_url(is_active=True)
    repository = create_repository(url)
    lifecycle = URLLifecycle(repository)

    result = lifecycle.deactivate(1)

    assert result.is_active is False
    repository.update.assert_called_once_with(url)


def test_deactivate_inactive_url_raises_error() -> None:
    """Deactivating an inactive URL should fail."""
    url = create_url(is_active=False)
    repository = create_repository(url)
    lifecycle = URLLifecycle(repository)

    with pytest.raises(URLAlreadyInactiveError):
        lifecycle.deactivate(1)


def test_activate_inactive_non_expired_url() -> None:
    """An inactive, non-expired URL should become active."""
    expiration = datetime.now(timezone.utc) + timedelta(hours=1)
    url = create_url(
        is_active=False,
        expires_at=expiration,
    )
    repository = create_repository(url)
    lifecycle = URLLifecycle(repository)

    result = lifecycle.activate(1)

    assert result.is_active is True
    repository.update.assert_called_once_with(url)


def test_activate_active_url_raises_error() -> None:
    """Activating an already active URL should fail."""
    url = create_url(is_active=True)
    repository = create_repository(url)
    lifecycle = URLLifecycle(repository)

    with pytest.raises(URLAlreadyActiveError):
        lifecycle.activate(1)


def test_activate_expired_url_raises_error() -> None:
    """An expired URL should not be reactivated."""
    expiration = datetime.now(timezone.utc) - timedelta(hours=1)
    url = create_url(
        is_active=False,
        expires_at=expiration,
    )
    repository = create_repository(url)
    lifecycle = URLLifecycle(repository)

    with pytest.raises(URLExpiredError):
        lifecycle.activate(1)


def test_delete_soft_deletes_url() -> None:
    """Deleting a URL should retain it while marking it inactive."""
    url = create_url(is_active=True)
    repository = create_repository(url)
    lifecycle = URLLifecycle(repository)

    result = lifecycle.delete(1)

    assert result is url
    assert result.is_active is False
    repository.update.assert_called_once_with(url)