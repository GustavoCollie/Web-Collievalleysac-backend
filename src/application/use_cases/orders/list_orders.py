from uuid import UUID

from domain.entities.order import Order
from domain.ports.repositories.order_repository import OrderRepository


class ListOrdersUseCase:
    def __init__(self, order_repo: OrderRepository):
        self._order_repo = order_repo

    async def execute(self, user_id: UUID) -> list[Order]:
        return await self._order_repo.find_by_user(user_id)
