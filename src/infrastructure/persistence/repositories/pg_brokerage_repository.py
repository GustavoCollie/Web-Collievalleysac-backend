from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.brokerage import BrokerageRequest, BrokerageStatus
from domain.ports.repositories.brokerage_repository import BrokerageRepository
from infrastructure.persistence.models.brokerage_model import BrokerageRequestORM


class PgBrokerageRepository(BrokerageRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    def _to_domain(self, orm: BrokerageRequestORM) -> BrokerageRequest:
        return BrokerageRequest(
            id=orm.id,
            user_id=orm.user_id,
            origin_country=orm.origin_country,
            dest_country=orm.dest_country,
            product_type=orm.product_type or "",
            volume_kg=float(orm.volume_kg),
            certifications=orm.certifications or [],
            status=BrokerageStatus(orm.status),
            quoted_price=float(orm.quoted_price) if orm.quoted_price else None,
            notes=orm.notes or "",
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    async def save(self, request: BrokerageRequest) -> BrokerageRequest:
        orm = BrokerageRequestORM(
            id=request.id,
            user_id=request.user_id,
            origin_country=request.origin_country,
            dest_country=request.dest_country,
            product_type=request.product_type,
            volume_kg=request.volume_kg,
            certifications=request.certifications,
            status=request.status.value,
            quoted_price=request.quoted_price,
            notes=request.notes,
        )
        self._session.add(orm)
        await self._session.commit()
        await self._session.refresh(orm)
        return self._to_domain(orm)

    async def find_by_id(self, request_id: UUID) -> BrokerageRequest | None:
        orm = await self._session.get(BrokerageRequestORM, request_id)
        return self._to_domain(orm) if orm else None

    async def find_by_user(self, user_id: UUID) -> list[BrokerageRequest]:
        stmt = (
            select(BrokerageRequestORM)
            .where(BrokerageRequestORM.user_id == user_id)
            .order_by(BrokerageRequestORM.created_at.desc())
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(orm) for orm in result.scalars().all()]

    async def update(self, request: BrokerageRequest) -> BrokerageRequest:
        orm = await self._session.get(BrokerageRequestORM, request.id)
        if orm:
            orm.status = request.status.value
            orm.quoted_price = request.quoted_price
            orm.notes = request.notes
            await self._session.commit()
            await self._session.refresh(orm)
            return self._to_domain(orm)
        return request
