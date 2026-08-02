from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr
from config import get_db_url

#  Получение url базы данных и последующее создание движка для подключения к БД
DATABASE_URL = get_db_url()
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"


async def get_session():
    async with async_session_maker() as session:
        yield session