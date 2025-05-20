from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from config import DATABASE_URL

engine = create_async_engine(
    url=DATABASE_URL, future=True, pool_size=10, max_overflow=20, pool_recycle=3600
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_maker() as session:
        yield session
