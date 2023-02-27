from typing import AsyncGenerator

from settings import get_settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker


# settings = get_settings()
postgres_database_url = "postgresql+asyncpg://kwame:rexosei111@127.0.0.1:5432/test_db"

engine = create_async_engine(postgres_database_url, future=True, echo=True)

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=True
)


class Base(DeclarativeBase):
    pass


async def create_db_tables():
    async with engine.begin() as conn:
        print("creating tables...")
        await conn.run_sync(Base.metadata.create_all)


async def drop_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
