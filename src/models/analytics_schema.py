"""
Project : URL Shortener API

Project ID : 018

Analytics Schemas
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class URLAnalyticsResponse(BaseModel):
    """Response containing click analytics for a shortened URL."""

    model_config = ConfigDict(from_attributes=True)

    url_id: int
    short_code: str
    total_clicks: int
    first_clicked_at: datetime | None
    last_clicked_at: datetime | None