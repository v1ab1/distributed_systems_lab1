from app.services import PersonsService
from app.db.engine import get_db
from app.infrastructure.repositories import PersonsRepository


async def get_persons_service() -> PersonsService:  # type: ignore
    async for session in get_db():
        persons_repository = PersonsRepository(session)

        return PersonsService(persons_repository)
