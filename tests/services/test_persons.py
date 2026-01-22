from unittest.mock import AsyncMock

import pytest

from app.services.persons import PersonsService
from app.services.exceptions import PersonNotFoundError
from app.presentation.api.schemas import PersonResponseSchema, PersonCreateRequestSchema


class TestPersonsService:
    @pytest.fixture
    def mock_repository(self):
        return AsyncMock()

    @pytest.fixture
    def persons_service(self, mock_repository):
        return PersonsService(mock_repository)

    @pytest.fixture
    def get_person_response(self):
        return PersonResponseSchema(
            id=1,
            name="Иван Иванович",
            age=30,
            address="Москва",
            work="Разработчик",
        )

    @pytest.fixture
    def save_person_response(self):
        return PersonCreateRequestSchema(
            name="Петр Петров",
            age=25,
            address="Санкт-Петербург",
            work="Тестировщик",
        )

    @pytest.mark.asyncio
    async def test_get_all_persons(self, persons_service, mock_repository, get_person_response):
        expected_persons = [get_person_response]
        mock_repository.get_all.return_value = expected_persons

        result = await persons_service.get_all()

        assert result == expected_persons
        mock_repository.get_all.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_person_by_id_success(self, persons_service, mock_repository, get_person_response):
        person_id = 1
        mock_repository.get_by_id.return_value = get_person_response

        result = await persons_service.get_by_id(person_id)

        assert result == get_person_response
        assert result.id == person_id
        mock_repository.get_by_id.assert_called_once_with(person_id)

    @pytest.mark.asyncio
    async def test_get_person_by_id_not_found(self, persons_service, mock_repository):
        person_id = 999
        mock_repository.get_by_id.side_effect = PersonNotFoundError(person_id)

        with pytest.raises(PersonNotFoundError) as exc_info:
            await persons_service.get_by_id(person_id)

        assert exc_info.value.person_id == person_id
        mock_repository.get_by_id.assert_called_once_with(person_id)

    @pytest.mark.asyncio
    async def test_save_new_person(self, persons_service, mock_repository, save_person_response):
        expected_id = 42
        mock_repository.save_new_person.return_value = expected_id

        result_id = await persons_service.save_new_person(save_person_response)

        assert result_id == expected_id
        mock_repository.save_new_person.assert_called_once_with(save_person_response)

    @pytest.mark.asyncio
    async def test_update_person_success(self, persons_service, mock_repository, save_person_response):
        person_id = 1
        mock_repository.update_person.return_value = None

        await persons_service.update_person(person_id, save_person_response)

        mock_repository.update_person.assert_called_once_with(person_id, save_person_response)

    @pytest.mark.asyncio
    async def test_delete_person_success(self, persons_service, mock_repository):
        person_id = 1
        mock_repository.delete_person.return_value = None

        await persons_service.delete_person(person_id)

        mock_repository.delete_person.assert_called_once_with(person_id)
