from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import routers
from app.logger import persons_logger
from app.db.engine import init_db
from app.presentation.api import handlers


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore
    """Lifecycle события приложения."""
    import asyncio

    persons_logger.info("Запуск приложения...")

    await asyncio.sleep(2)

    try:
        await init_db()
        persons_logger.info("Инициализация БД завершена успешно")
    except Exception as e:
        persons_logger.error(f"Ошибка при инициализации БД: {e}", exc_info=True)
        persons_logger.warning("Приложение запускается без инициализации БД")
    yield
    persons_logger.info("Остановка приложения...")


app = FastAPI(
    title="Persons services",
    description="Сервис, который предоставляет CRUD операции над пользователями",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_prefix="/api",
    lifespan=lifespan,
)

routers.add_routers(app)
handlers.add_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
