from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.brokerage import BrokerageRequest


class BrokerageRepository(ABC):
    @abstractmethod
    async def save(self, request: BrokerageRequest) -> BrokerageRequest: ...

    @abstractmethod
    async def find_by_id(self, request_id: UUID) -> BrokerageRequest | None: ...

    @abstractmethod
    async def find_by_user(self, user_id: UUID) -> list[BrokerageRequest]: ...

    @abstractmethod
    async def update(self, request: BrokerageRequest) -> BrokerageRequest: ...
