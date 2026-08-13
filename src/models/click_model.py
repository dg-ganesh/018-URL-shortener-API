"""
Project : URL Shortener API

Project ID : 018

URL Click Database Model
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from src.models.url_model import Base


class URLClick(Base):
    """Database model representing a successful URL click."""

    __tablename__ = "url_clicks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    url_id: Mapped[int] = mapped_column(
        ForeignKey("urls.id"),
        nullable=False,
        index=True,
    )

    clicked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )