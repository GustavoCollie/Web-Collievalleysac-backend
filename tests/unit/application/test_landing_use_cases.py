import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from domain.entities.landing_section import LandingSection
from domain.exceptions.base import EntityNotFound
from application.dtos.landing_dto import CreateSectionInput, UpdateSectionInput
from application.use_cases.landing.get_landing_sections import GetLandingSectionsUseCase
from application.use_cases.landing.update_landing_section import (
    CreateLandingSectionUseCase,
    UpdateLandingSectionUseCase,
    DeleteLandingSectionUseCase,
)


@pytest.fixture
def mock_landing_repo():
    return AsyncMock()


class TestGetLandingSections:
    @pytest.mark.asyncio
    async def test_get_visible_sections(self, mock_landing_repo):
        sections = [
            LandingSection(section_key="hero", title="Hero Section"),
            LandingSection(section_key="products", title="Products"),
        ]
        mock_landing_repo.find_all_visible.return_value = sections

        use_case = GetLandingSectionsUseCase(mock_landing_repo)
        result = await use_case.execute(include_hidden=False)

        assert len(result) == 2
        mock_landing_repo.find_all_visible.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_sections(self, mock_landing_repo):
        mock_landing_repo.find_all.return_value = []

        use_case = GetLandingSectionsUseCase(mock_landing_repo)
        result = await use_case.execute(include_hidden=True)

        assert len(result) == 0
        mock_landing_repo.find_all.assert_called_once()


class TestCreateLandingSection:
    @pytest.mark.asyncio
    async def test_create_section(self, mock_landing_repo):
        mock_landing_repo.save.return_value = LandingSection(
            section_key="hero", title="Mi Hero"
        )

        use_case = CreateLandingSectionUseCase(mock_landing_repo)
        result = await use_case.execute(
            CreateSectionInput(section_key="hero", title="Mi Hero")
        )

        assert result.section_key == "hero"
        assert result.title == "Mi Hero"


class TestUpdateLandingSection:
    @pytest.mark.asyncio
    async def test_update_section(self, mock_landing_repo):
        existing = LandingSection(section_key="hero", title="Old Title")
        mock_landing_repo.find_by_key.return_value = existing
        mock_landing_repo.update.return_value = LandingSection(
            section_key="hero", title="New Title"
        )

        use_case = UpdateLandingSectionUseCase(mock_landing_repo)
        result = await use_case.execute(
            UpdateSectionInput(section_key="hero", title="New Title")
        )

        assert result.title == "New Title"

    @pytest.mark.asyncio
    async def test_update_nonexistent_section(self, mock_landing_repo):
        mock_landing_repo.find_by_key.return_value = None

        use_case = UpdateLandingSectionUseCase(mock_landing_repo)
        with pytest.raises(EntityNotFound):
            await use_case.execute(
                UpdateSectionInput(section_key="nonexistent", title="X")
            )


class TestDeleteLandingSection:
    @pytest.mark.asyncio
    async def test_delete_section(self, mock_landing_repo):
        existing = LandingSection(section_key="old", title="Old")
        mock_landing_repo.find_by_key.return_value = existing

        use_case = DeleteLandingSectionUseCase(mock_landing_repo)
        await use_case.execute("old")

        mock_landing_repo.delete.assert_called_once_with(existing.id)

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, mock_landing_repo):
        mock_landing_repo.find_by_key.return_value = None

        use_case = DeleteLandingSectionUseCase(mock_landing_repo)
        with pytest.raises(EntityNotFound):
            await use_case.execute("nonexistent")
