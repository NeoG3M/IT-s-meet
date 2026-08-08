from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from .config import get_db_url

#  Получение url базы данных и последующее создание движка для подключения к БД
DATABASE_URL = get_db_url()
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with async_session_maker() as session:
        yield session


SessionDep = Annotated[
    AsyncSession,
    Depends(get_session)
]