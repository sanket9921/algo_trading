from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings
from app.storage.base import Base

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def initialize_database() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(
            Base.metadata.create_all
        )