from uuid import UUID

from domain.entities.product import Product
from domain.exceptions.base import EntityNotFound
from domain.ports.repositories.product_repository import ProductRepository
from application.dtos.product_dto import CreateProductInput


class CreateProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self._product_repo = product_repo

    async def execute(self, input: CreateProductInput) -> Product:
        product = Product(
            name=input.name,
            slug=input.slug,
            category=input.category,
            price_per_kg=input.price_per_kg,
            description=input.description,
            image_url=input.image_url,
            currency=input.currency,
            season_start=input.season_start,
            season_end=input.season_end,
            is_available=input.is_available,
        )
        return await self._product_repo.save(product)


class DeleteProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self._product_repo = product_repo

    async def execute(self, product_id: UUID) -> None:
        product = await self._product_repo.find_by_id(product_id)
        if not product:
            raise EntityNotFound("Producto", str(product_id))
        await self._product_repo.delete(product_id)
