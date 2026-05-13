from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.order import Order


class OrderRepository(ABC):
    @abstractmethod
    async def save(self, order: Order) -> Order: ...

    @abstractmethod
    async def find_by_id(self, order_id: UUID) -> Order | None: ...

    @abstractmethod
    async def find_by_user(self, user_id: UUID) -> list[Order]: ...

    @abstractmethod
    async def update(self, order: Order) -> Order: ...
