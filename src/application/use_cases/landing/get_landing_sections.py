from domain.entities.landing_section import LandingSection
from domain.ports.repositories.landing_repository import LandingRepository


class GetLandingSectionsUseCase:
    def __init__(self, landing_repo: LandingRepository):
        self._landing_repo = landing_repo

    async def execute(self, include_hidden: bool = False) -> list[LandingSection]:
        if include_hidden:
            return await self._landing_repo.find_all()
        return await self._landing_repo.find_all_visible()
