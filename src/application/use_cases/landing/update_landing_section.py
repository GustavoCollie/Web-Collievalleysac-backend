from domain.entities.landing_section import LandingSection
from domain.exceptions.base import EntityNotFound
from domain.ports.repositories.landing_repository import LandingRepository
from application.dtos.landing_dto import CreateSectionInput, UpdateSectionInput


class CreateLandingSectionUseCase:
    def __init__(self, landing_repo: LandingRepository):
        self._landing_repo = landing_repo

    async def execute(self, input: CreateSectionInput) -> LandingSection:
        section = LandingSection(
            section_key=input.section_key,
            title=input.title,
            subtitle=input.subtitle,
            content=input.content,
            display_order=input.display_order,
            is_visible=input.is_visible,
            updated_by=input.updated_by,
        )
        return await self._landing_repo.save(section)


class UpdateLandingSectionUseCase:
    def __init__(self, landing_repo: LandingRepository):
        self._landing_repo = landing_repo

    async def execute(self, input: UpdateSectionInput) -> LandingSection:
        existing = await self._landing_repo.find_by_key(input.section_key)
        if not existing:
            raise EntityNotFound("Sección", input.section_key)

        if input.title is not None:
            existing.title = input.title
        if input.subtitle is not None:
            existing.subtitle = input.subtitle
        if input.content is not None:
            existing.content = input.content
        if input.display_order is not None:
            existing.display_order = input.display_order
        if input.is_visible is not None:
            existing.is_visible = input.is_visible
        if input.updated_by is not None:
            existing.updated_by = input.updated_by

        return await self._landing_repo.update(existing)


class DeleteLandingSectionUseCase:
    def __init__(self, landing_repo: LandingRepository):
        self._landing_repo = landing_repo

    async def execute(self, section_key: str) -> None:
        existing = await self._landing_repo.find_by_key(section_key)
        if not existing:
            raise EntityNotFound("Sección", section_key)
        await self._landing_repo.delete(existing.id)
