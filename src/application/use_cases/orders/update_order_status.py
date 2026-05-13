from domain.entities.order import Order, OrderStatus
from domain.exceptions.base import EntityNotFound
from domain.exceptions.auth import InsufficientPermissions
from domain.exceptions.order import OrderNotModifiable
from domain.ports.repositories.order_repository import OrderRepository
from application.dtos.order_dto import UpdateOrderStatusInput

# Allowed transitions
ALLOWED_TRANSITIONS: dict[OrderStatus, list[OrderStatus]] = {
    OrderStatus.DRAFT: [OrderStatus.PENDING, OrderStatus.CANCELLED],
    OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
    OrderStatus.CONFIRMED: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
    OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
    OrderStatus.DELIVERED: [],
    OrderStatus.CANCELLED: [],
}


class UpdateOrderStatusUseCase:
    def __init__(self, order_repo: OrderRepository):
        self._order_repo = order_repo

    async def execute(self, input: UpdateOrderStatusInput) -> Order:
        order = await self._order_repo.find_by_id(input.order_id)
        if not order:
            raise EntityNotFound("Pedido", str(input.order_id))

        # Only the owner or admin can modify orders
        # (admin check handled at router level via RBAC)
        if order.user_id != input.user_id:
            raise InsufficientPermissions()

        new_status = OrderStatus(input.status)
        allowed = ALLOWED_TRANSITIONS.get(order.status, [])
        if new_status not in allowed:
            raise OrderNotModifiable()

        order.status = new_status
        return await self._order_repo.update(order)
