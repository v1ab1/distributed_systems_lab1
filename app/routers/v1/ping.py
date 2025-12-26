from fastapi import APIRouter

router = APIRouter(prefix="/v1/ping")


@router.get("")
def ping() -> str:
    return "ok"
