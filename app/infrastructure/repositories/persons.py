from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.persons import PersonsDB
from app.services.exceptions import PersonNotFoundError
from app.presentation.api.schemas import PersonResponseSchema, PersonCreateRequestSchema


class PersonsRepository:
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_all(self) -> list[PersonResponseSchema]:
        query = select(PersonsDB)
        result = await self._db.execute(query)
        persons_db = result.scalars().all()
        persons = [PersonResponseSchema.model_validate(person) for person in persons_db]
        return persons

    async def get_by_id(self, id: int) -> PersonResponseSchema:
        query = select(PersonsDB).where(PersonsDB.id == id)
        result = await self._db.execute(query)
        person = result.scalar_one_or_none()

        if person is None:
            raise PersonNotFoundError(id)

        return PersonResponseSchema.model_validate(person)

    async def save_new_person(self, person: PersonCreateRequestSchema) -> int:
        person_db = PersonsDB(**person.model_dump())
        self._db.add(person_db)
        await self._db.flush()
        person_id = person_db.id
        await self._db.commit()
        return int(person_id)

    async def delete_person(self, person_id: int) -> None:
        await self.get_by_id(person_id)
        await self._db.execute(delete(PersonsDB).where(PersonsDB.id == id))
        await self._db.commit()

    async def update_person(self, person_id: int, person_body: PersonCreateRequestSchema) -> None:
        person = await self._db.get(PersonsDB, person_id)
        if not person:
            raise PersonNotFoundError(person_id)
        for key, value in person_body.model_dump(exclude_unset=True).items():
            setattr(person, key, value)
        await self._db.commit()
        await self._db.refresh(person)
