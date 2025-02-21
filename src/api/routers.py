from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.apps.courses.routes.courses import course_router
from src.core.db.async_database import init_db
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for the FastAPI application.
    This function is used to manage the lifespan of the FastAPI application. It can be used to perform
    any setup or teardown tasks that need to occur when the application starts up or shuts down.
    Args:
        app (FastAPI): The FastAPI application instance.
    Yields:
        None: This function is a generator that yields control back to the FastAPI application.
    """
    await init_db()
    yield


version = "v1"
app = FastAPI(version=version, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],
)

app.include_router(course_router, prefix=f"/api/{version}")
