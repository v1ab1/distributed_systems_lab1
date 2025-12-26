from enum import Enum
from typing import Any, TypedDict

from fastapi import FastAPI, APIRouter

from app.routers.v1.ping import router as ping_router
from app.routers.v1.persons import router as persons_router


class RouterConfig(TypedDict):
    """Конфигурация роутера для регистрации в приложении."""

    router: APIRouter
    tags: list[str | Enum]
    dependencies: list[Any] | None


MIDDLEWARES = []  # type: ignore

routers: list[RouterConfig] = [
    {
        "router": ping_router,
        "tags": ["Ping"],
        "dependencies": MIDDLEWARES,
    },
    {"router": persons_router, "tags": ["Persons"], "dependencies": MIDDLEWARES},
]


def add_routers(app: FastAPI) -> None:
    for router_config in routers:
        app.include_router(
            router_config["router"], tags=router_config["tags"], dependencies=router_config["dependencies"]
        )
