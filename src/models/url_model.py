"""
Project : URL Shortener API

Project ID : 018

URL Database Model
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""


class URL(Base):
    """Database model representing a shortened URL."""

    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    original_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    short_code: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        unique=True,
        index=True,
    )

    custom_alias: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        unique=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )