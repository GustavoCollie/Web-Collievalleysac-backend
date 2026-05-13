from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.entities.order import Order, OrderItem, OrderStatus
from domain.ports.repositories.order_repository import OrderRepository
from infrastructure.persistence.models.order_model import OrderItemORM, OrderORM


class PgOrderRepository(OrderRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    def _to_domain(self, orm: OrderORM) -> Order:
        items = [
            OrderItem(
                id=item.id,
                product_id=item.product_id,
                quantity_kg=float(item.quantity_kg),
                quality_grade=item.quality_grade,
                unit_price=float(item.unit_price),
            )
            for item in (orm.items or [])
        ]
        return Order(
            id=orm.id,
            user_id=orm.user_id,
            items=items if items else [OrderItem(product_id=orm.user_id, quantity_kg=0, quality_grade="N/A", unit_price=0)],
            status=OrderStatus(orm.status),
            currency=orm.currency,
            delivery_date=orm.delivery_date,
            shipping_address=orm.shipping_address or "",
            notes=orm.notes or "",
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    async def save(self, order: Order) -> Order:
        orm = OrderORM(
            id=order.id,
            user_id=order.user_id,
            status=order.status.value,
            total_amount=order.total_amount,
            currency=order.currency,
            delivery_date=order.delivery_date,
            shipping_address=order.shipping_address,
            notes=order.notes,
        )
        orm.items = [
            OrderItemORM(
                id=item.id,
                product_id=item.product_id,
                quantity_kg=item.quantity_kg,
                quality_grade=item.quality_grade,
                unit_price=item.unit_price,
                subtotal=item.subtotal,
            )
            for item in order.items
        ]
        self._session.add(orm)
        await self._session.commit()

        # Reload with items
        stmt = (
            select(OrderORM)
            .options(selectinload(OrderORM.items))
            .where(OrderORM.id == order.id)
        )
        result = await self._session.execute(stmt)
        refreshed = result.scalar_one()
        return self._to_domain(refreshed)

    async def find_by_id(self, order_id: UUID) -> Order | None:
        stmt = (
            select(OrderORM)
            .options(selectinload(OrderORM.items))
            .where(OrderORM.id == order_id)
        )
        result = await self._session.execute(stmt)
        orm = result.scalar_one_or_none()
        return self._to_domain(orm) if orm else None

    async def find_by_user(self, user_id: UUID) -> list[Order]:
        stmt = (
            select(OrderORM)
            .options(selectinload(OrderORM.items))
            .where(OrderORM.user_id == user_id)
            .order_by(OrderORM.created_at.desc())
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(orm) for orm in result.scalars().all()]

    async def update(self, order: Order) -> Order:
        orm = await self._session.get(OrderORM, order.id)
        if orm:
            orm.status = order.status.value
            orm.total_amount = order.total_amount
            orm.delivery_date = order.delivery_date
            orm.shipping_address = order.shipping_address
            orm.notes = order.notes
            await self._session.commit()

            stmt = (
                select(OrderORM)
                .options(selectinload(OrderORM.items))
                .where(OrderORM.id == order.id)
            )
            result = await self._session.execute(stmt)
            refreshed = result.scalar_one()
            return self._to_domain(refreshed)
        return order
