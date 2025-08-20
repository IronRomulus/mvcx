import os
from typing import Annotated, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from mvcx.di import depends

DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite+aiosqlite:///mvcx.db"

_engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

_DbSession = async_sessionmaker(_engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = _DbSession()
    try:
        async with db.begin():
            yield db
    finally:
        await db.close()


DbSession = Annotated[AsyncSession, depends(get_db)]
