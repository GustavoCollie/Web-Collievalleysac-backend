from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.advisory import AdvisoryRequest, TechnicalArticle


class AdvisoryRepository(ABC):
    @abstractmethod
    async def save(self, request: AdvisoryRequest) -> AdvisoryRequest: ...

    @abstractmethod
    async def find_by_id(self, request_id: UUID) -> AdvisoryRequest | None: ...

    @abstractmethod
    async def find_by_user(self, user_id: UUID) -> list[AdvisoryRequest]: ...

    @abstractmethod
    async def update(self, request: AdvisoryRequest) -> AdvisoryRequest: ...


class ArticleRepository(ABC):
    @abstractmethod
    async def find_all(self, crop_tags: list[str] | None = None) -> list[TechnicalArticle]: ...

    @abstractmethod
    async def find_by_slug(self, slug: str) -> TechnicalArticle | None: ...

    @abstractmethod
    async def save(self, article: TechnicalArticle) -> TechnicalArticle: ...
