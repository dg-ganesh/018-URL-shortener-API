"""
Project : URL Shortener API

Project ID : 018

Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.health_routes import router as health_router
from src.api.redirect_routes import router as redirect_router
from src.api.url_routes import router as url_router
from src.config import get_settings
from src.services.database_service import initialize_database
from src.utils.logger import create_execution_logger


settings = get_settings()
execution_logger = create_execution_logger()


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""

    application = FastAPI(
        title=settings.project_name,
        version=settings.app_version,
        description=(
            "REST API for creating and managing shortened URLs."
        ),
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5500",
            "http://127.0.0.1:5500",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(health_router)
    application.include_router(url_router)
    application.include_router(redirect_router)

    return application


app = create_application()


@app.on_event("startup")
def application_startup() -> None:
    """Initialize application resources during startup."""

    execution_logger.start()

    try:
        execution_logger.checkpoint(
            "Configuration loaded successfully."
        )

        initialize_database()

        execution_logger.checkpoint(
            "Database initialization completed."
        )

        execution_logger.checkpoint(
            "API application startup completed."
        )

        execution_logger.write_report()

    except Exception as exc:
        execution_logger.record_error(exc)
        execution_logger.write_report()

        raise


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )