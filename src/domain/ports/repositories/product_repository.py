from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.product import Product


class ProductRepository(ABC):
    @abstractmethod
    async def save(self, product: Product) -> Product: ...

    @abstractmethod
    async def find_by_id(self, product_id: UUID) -> Product | None: ...

    @abstractmethod
    async def find_available(self, month: int | None = None) -> list[Product]: ...

    @abstractmethod
    async def update(self, product: Product) -> Product: ...

    @abstractmethod
    async def delete(self, product_id: UUID) -> None: ...
