from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.landing_section import LandingSection


class LandingRepository(ABC):
    @abstractmethod
    async def find_all_visible(self) -> list[LandingSection]: ...

    @abstractmethod
    async def find_all(self) -> list[LandingSection]: ...

    @abstractmethod
    async def find_by_key(self, section_key: str) -> LandingSection | None: ...

    @abstractmethod
    async def save(self, section: LandingSection) -> LandingSection: ...

    @abstractmethod
    async def update(self, section: LandingSection) -> LandingSection: ...

    @abstractmethod
    async def delete(self, section_id: UUID) -> None: ...
