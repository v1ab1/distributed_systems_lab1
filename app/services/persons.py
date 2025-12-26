from app.presentation.api.schemas import PersonResponseSchema, PersonCreateRequestSchema
from app.infrastructure.repositories import PersonsRepository


class PersonsService:
    def __init__(self, persons_repository: PersonsRepository):
        self._persons_repository = persons_repository

    async def get_all(self) -> list[PersonResponseSchema]:
        return await self._persons_repository.get_all()

    async def get_by_id(self, id: int) -> PersonResponseSchema:
        return await self._persons_repository.get_by_id(id)

    async def save_new_person(self, person: PersonCreateRequestSchema) -> int:
        id = await self._persons_repository.save_new_person(person)
        return id

    async def delete_person(self, person_id: int) -> None:
        await self._persons_repository.delete_person(person_id)

    async def update_person(self, person_id: int, person: PersonCreateRequestSchema) -> None:
        await self._persons_repository.update_person(person_id, person)
