from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.apps.courses.routes.courses import course_router
from src.apps.auth.routes.auth import auth_router
from src.core.db.async_database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles application startup and shutdown lifecycle events."""
    await init_db()
    yield


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application."""
    app = FastAPI(version="v1", lifespan=lifespan)

    # CORS middleware configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Update this with your frontend URL for security
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],
    )

    # Register routes
    include_routes(app, "v1")

    return app


def include_routes(app: FastAPI, version: str):
    """Includes all application routers with a common API version prefix."""
    api_prefix = f"/api/{version}"
    app.include_router(course_router, prefix=api_prefix)
    app.include_router(auth_router, prefix=api_prefix)


app = create_app()
