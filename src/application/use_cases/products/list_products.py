from domain.entities.product import Product
from domain.ports.repositories.product_repository import ProductRepository


class ListProductsUseCase:
    def __init__(self, product_repo: ProductRepository):
        self._product_repo = product_repo

    async def execute(self, month: int | None = None) -> list[Product]:
        return await self._product_repo.find_available(month=month)
