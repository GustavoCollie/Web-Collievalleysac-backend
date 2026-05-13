from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.product import Product
from domain.ports.repositories.product_repository import ProductRepository
from infrastructure.persistence.models.product_model import ProductORM


class PgProductRepository(ProductRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    def _to_domain(self, orm: ProductORM) -> Product:
        return Product(
            id=orm.id,
            name=orm.name,
            slug=orm.slug,
            description=orm.description or "",
            category=orm.category or "",
            image_url=orm.image_url or "",
            price_per_kg=float(orm.price_per_kg),
            currency=orm.currency,
            season_start=orm.season_start,
            season_end=orm.season_end,
            is_available=orm.is_available,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    async def save(self, product: Product) -> Product:
        orm = ProductORM(
            id=product.id,
            name=product.name,
            slug=product.slug,
            description=product.description,
            category=product.category,
            image_url=product.image_url,
            price_per_kg=product.price_per_kg,
            currency=product.currency,
            season_start=product.season_start,
            season_end=product.season_end,
            is_available=product.is_available,
        )
        self._session.add(orm)
        await self._session.commit()
        await self._session.refresh(orm)
        return self._to_domain(orm)

    async def find_by_id(self, product_id: UUID) -> Product | None:
        orm = await self._session.get(ProductORM, product_id)
        return self._to_domain(orm) if orm else None

    async def find_available(self, month: int | None = None) -> list[Product]:
        stmt = select(ProductORM).where(ProductORM.is_available == True)
        if month is not None:
            stmt = stmt.where(
                ProductORM.season_start <= month,
                ProductORM.season_end >= month,
            )
        stmt = stmt.order_by(ProductORM.name)
        result = await self._session.execute(stmt)
        return [self._to_domain(orm) for orm in result.scalars().all()]

    async def update(self, product: Product) -> Product:
        orm = await self._session.get(ProductORM, product.id)
        if orm:
            orm.name = product.name
            orm.slug = product.slug
            orm.description = product.description
            orm.category = product.category
            orm.image_url = product.image_url
            orm.price_per_kg = product.price_per_kg
            orm.currency = product.currency
            orm.season_start = product.season_start
            orm.season_end = product.season_end
            orm.is_available = product.is_available
            await self._session.commit()
            await self._session.refresh(orm)
            return self._to_domain(orm)
        return product

    async def delete(self, product_id: UUID) -> None:
        orm = await self._session.get(ProductORM, product_id)
        if orm:
            await self._session.delete(orm)
            await self._session.commit()
