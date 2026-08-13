"""
Project : URL Shortener API

Project ID : 018

URL Alias Validator
"""

import re


class InvalidAliasError(Exception):
    """Raised when a custom URL alias is invalid."""


class AliasValidator:
    """Validate custom aliases for shortened URLs."""

    MIN_LENGTH = 3
    MAX_LENGTH = 50

    _ALIAS_PATTERN = re.compile(
        r"^[A-Za-z0-9](?:[A-Za-z0-9_-]*[A-Za-z0-9])?$"
    )

    def validate(self, alias: str) -> str:
        """
        Validate and normalize a custom alias.

        Returns:
            The normalized alias.

        Raises:
            InvalidAliasError:
                If the alias is empty, too short, too long,
                or contains unsupported characters.
        """
        normalized_alias = alias.strip()

        if not normalized_alias:
            raise InvalidAliasError(
                "Custom alias cannot be empty."
            )

        if len(normalized_alias) < self.MIN_LENGTH:
            raise InvalidAliasError(
                f"Custom alias must contain at least "
                f"{self.MIN_LENGTH} characters."
            )

        if len(normalized_alias) > self.MAX_LENGTH:
            raise InvalidAliasError(
                f"Custom alias cannot contain more than "
                f"{self.MAX_LENGTH} characters."
            )

        if not self._ALIAS_PATTERN.fullmatch(normalized_alias):
            raise InvalidAliasError(
                "Custom alias may contain only letters, "
                "numbers, hyphens, and underscores, and must "
                "start and end with a letter or number."
            )

        return normalized_alias
    