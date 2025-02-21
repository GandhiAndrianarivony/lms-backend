from sqlmodel import create_engine, text
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker

from src.configs.database_configs import pg_configs


DATABASE_URL = f"postgresql+asyncpg://{pg_configs.USER}:{pg_configs.PASSWORD}@{pg_configs.HOST}:{pg_configs.PORT}/{pg_configs.DB}"

async_engine = AsyncEngine(
    create_engine(
        url=DATABASE_URL,
        echo=True,
    )
)


async def init_db():
    """
    Initialize the database connection and execute a test query.
    This asynchronous function establishes a connection to the database using
    the provided engine, executes a simple "Hello world!" SQL statement, and
    prints the result.
    Returns:
        None
    """
    
    async with async_engine.begin() as conn:
        statement = text("SELECT 'Hello world!';")
        result = await conn.execute(statement)
        print(result.all())




async def get_session_db() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(
        bind=async_engine, 
        autocommit=False,
        expire_on_commit=True,
        class_=AsyncSession
    )
    async with Session() as session:
        yield session