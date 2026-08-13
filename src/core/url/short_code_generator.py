"""
Project : URL Shortener API

Project ID : 018

Short Code Generator
"""

import secrets
import string


class ShortCodeGenerator:
    """Generate cryptographically random Base62 short codes."""

    _CHARACTERS = string.ascii_letters + string.digits

    def __init__(self, length: int = 7) -> None:
        """
        Initialize the generator.

        Args:
            length: Number of characters in each generated short code.
        """
        if length < 4:
            raise ValueError("Short-code length must be at least 4.")

        if length > 32:
            raise ValueError("Short-code length must not exceed 32.")

        self._length = length

    @property
    def length(self) -> int:
        """Return the configured short-code length."""
        return self._length

    def generate(self) -> str:
        """Generate and return a random Base62 short code."""
        return "".join(
            secrets.choice(self._CHARACTERS)
            for _ in range(self._length)
        )


def generate_short_code(length: int = 7) -> str:
    """Generate a short code using the default generator."""
    generator = ShortCodeGenerator(length=length)

    return generator.generate()
