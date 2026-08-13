"""
Project : URL Shortener API

Project ID : 018

Database Service
"""

from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from src.config import get_settings


settings = get_settings()

engine: Engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_database_session() -> Generator[Session, None, None]:
    """
    Provide a database session and ensure it is closed after use.
    """
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


def check_database_connection() -> bool:
    """
    Verify that the configured database is reachable.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return True

    except Exception:
        return False


def initialize_database() -> None:
    """
    Initialize database tables and apply required schema changes.

    The model metadata imports are intentionally performed inside
    this function to avoid circular imports during application
    startup.
    """
    from src.models.click_model import URLClick
    from src.models.url_model import Base

    # Ensure the click model is registered with SQLAlchemy metadata.
    _ = URLClick

    Base.metadata.create_all(bind=engine)

    _ensure_url_expiration_column()
    _ensure_custom_alias_column()


def _ensure_url_expiration_column() -> None:
    """
    Ensure the URL expiration column exists.

    Existing databases require this schema change because
    SQLAlchemy create_all() does not modify existing tables.
    """
    statement = text(
        """
        ALTER TABLE urls
        ADD COLUMN IF NOT EXISTS expires_at
        TIMESTAMP WITH TIME ZONE
        """
    )

    with engine.begin() as connection:
        connection.execute(statement)


def _ensure_custom_alias_column() -> None:
    """
    Ensure the custom alias column and unique index exist.

    Existing databases require this schema change because
    SQLAlchemy create_all() does not modify existing tables.
    """
    add_column_statement = text(
        """
        ALTER TABLE urls
        ADD COLUMN IF NOT EXISTS custom_alias
        VARCHAR(50)
        """
    )

    create_index_statement = text(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS
        ix_urls_custom_alias
        ON urls (custom_alias)
        """
    )

    with engine.begin() as connection:
        connection.execute(add_column_statement)
        connection.execute(create_index_statement)


def dispose_database_engine() -> None:
    """
    Dispose of the SQLAlchemy engine and its connection pool.
    """
    engine.dispose()