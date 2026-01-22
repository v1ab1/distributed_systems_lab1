import os

from functools import lru_cache
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.logger import persons_logger

load_dotenv(override=True)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_database_url() -> str:
    url = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    persons_logger.info(
        "Подключение к БД: postgresql+asyncpg://%s@%s:%s/%s",
        DB_USER,
        DB_HOST,
        DB_PORT,
        DB_NAME,
    )
    return url


@lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    database_url = get_database_url()
    engine = create_async_engine(
        database_url,
        echo=True,
        pool_pre_ping=True,
        pool_size=1000,
        max_overflow=1000,
        connect_args={"timeout": 5},
    )
    return engine


@lru_cache(maxsize=1)
def get_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autoflush=False,
    )


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    engine = get_engine()
    sessionmaker = get_sessionmaker(engine)
    async with sessionmaker() as session:
        yield session
        await session.close()


@asynccontextmanager
async def lazy_db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = get_engine()
    sessionmaker = get_sessionmaker(engine)
    async with sessionmaker() as session:
        yield session
        await session.close()


async def init_db() -> None:
    import asyncio

    from sqlalchemy import text

    import app.db.models  # noqa: F401

    from app.db.base import Base

    max_retries = 10
    retry_delay = 2

    persons_logger.info("Начало инициализации БД...")

    for attempt in range(max_retries):
        try:
            persons_logger.info(f"Попытка {attempt + 1}/{max_retries} подключения к БД...")
            engine = get_engine()

            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))

            persons_logger.info("Подключение к БД установлено, создаём таблицы...")

            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            persons_logger.info("✅ Таблицы успешно созданы в БД")

            async with engine.connect() as conn:
                result = await conn.execute(
                    text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
                )
                tables = [row[0] for row in result]
                persons_logger.info(f"Созданные таблицы: {', '.join(tables) if tables else 'нет таблиц'}")

            return
        except Exception as e:
            if attempt < max_retries - 1:
                persons_logger.warning(
                    f"Попытка {attempt + 1}/{max_retries} подключения к БД не удалась: {e}. "
                    f"Повтор через {retry_delay} секунд..."
                )
                await asyncio.sleep(retry_delay)
            else:
                persons_logger.error(
                    f"❌ Не удалось инициализировать БД после {max_retries} попыток: {e}", exc_info=True
                )
                raise
