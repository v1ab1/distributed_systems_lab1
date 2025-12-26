from typing import TYPE_CHECKING

from fastapi import Depends, Response, APIRouter

from app.dependencies import get_persons_service
from app.presentation.api.schemas import PersonResponseSchema, PersonCreateRequestSchema

if TYPE_CHECKING:
    from app.services.persons import PersonsService

router = APIRouter(prefix="/v1/persons")


@router.get("")
async def get_all_persons(
    persons_service: "PersonsService" = Depends(get_persons_service),
) -> list[PersonResponseSchema]:
    persons = await persons_service.get_all()
    return persons


@router.post("", status_code=201)
async def save_new_person(
    body: PersonCreateRequestSchema,
    response: Response,
    persons_service: "PersonsService" = Depends(get_persons_service),
) -> None:
    person_id = await persons_service.save_new_person(body)
    response.headers["Location"] = f"/api/v1/persons/{person_id}"
    return None


@router.get("/{person_id}")
async def get_person_by_id(
    person_id: int, persons_service: "PersonsService" = Depends(get_persons_service)
) -> PersonResponseSchema | None:
    return await persons_service.get_by_id(person_id)


@router.patch("/{person_id}", status_code=200)
async def update_person_by_id(
    person_id: int, body: PersonCreateRequestSchema, persons_service: "PersonsService" = Depends(get_persons_service)
) -> None:
    await persons_service.update_person(person_id, body)


@router.delete("/{person_id}", status_code=204)
async def delete_person_by_id(person_id: int, persons_service: "PersonsService" = Depends(get_persons_service)) -> None:
    await persons_service.delete_person(person_id)
