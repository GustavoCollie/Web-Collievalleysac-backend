from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.middleware.rbac_middleware import require_role
from api.schemas.order_schemas import (
    CreateOrderRequest,
    OrderListResponse,
    OrderResponse,
    UpdateOrderStatusRequest,
)
from application.dtos.order_dto import CreateOrderInput, OrderItemInput, UpdateOrderStatusInput
from application.use_cases.orders.create_order import CreateOrderUseCase
from application.use_cases.orders.list_orders import ListOrdersUseCase
from application.use_cases.orders.update_order_status import UpdateOrderStatusUseCase
from infrastructure.persistence.database import get_session
from infrastructure.persistence.repositories.pg_order_repository import PgOrderRepository
from infrastructure.persistence.repositories.pg_product_repository import PgProductRepository

router = APIRouter(prefix="/orders", tags=["orders"])


def _get_order_repo(session: AsyncSession = Depends(get_session)):
    return PgOrderRepository(session)


def _get_product_repo(session: AsyncSession = Depends(get_session)):
    return PgProductRepository(session)


@router.post("", response_model=OrderResponse, status_code=201)
async def create_order(
    request: CreateOrderRequest,
    user=Depends(require_role("importador")),
    order_repo=Depends(_get_order_repo),
    product_repo=Depends(_get_product_repo),
):
    user_id, _ = user
    use_case = CreateOrderUseCase(order_repo, product_repo)
    order = await use_case.execute(
        CreateOrderInput(
            user_id=user_id,
            items=[
                OrderItemInput(
                    product_id=UUID(item.product_id),
                    quantity_kg=item.quantity_kg,
                    quality_grade=item.quality_grade,
                )
                for item in request.items
            ],
            delivery_date=request.delivery_date,
            shipping_address=request.shipping_address,
            notes=request.notes,
        )
    )
    return OrderResponse.from_entity(order)


@router.get("", response_model=OrderListResponse)
async def list_my_orders(
    user=Depends(require_role("importador")),
    order_repo=Depends(_get_order_repo),
):
    user_id, _ = user
    use_case = ListOrdersUseCase(order_repo)
    orders = await use_case.execute(user_id)
    return OrderListResponse(
        orders=[OrderResponse.from_entity(o) for o in orders],
        total=len(orders),
    )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: UUID,
    user=Depends(require_role("importador")),
    order_repo=Depends(_get_order_repo),
):
    user_id, _ = user
    from domain.exceptions.base import EntityNotFound
    from domain.exceptions.auth import InsufficientPermissions

    order = await order_repo.find_by_id(order_id)
    if not order:
        raise EntityNotFound("Pedido", str(order_id))
    if order.user_id != user_id:
        raise InsufficientPermissions()
    return OrderResponse.from_entity(order)


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: UUID,
    request: UpdateOrderStatusRequest,
    user=Depends(require_role("importador")),
    order_repo=Depends(_get_order_repo),
):
    user_id, _ = user
    use_case = UpdateOrderStatusUseCase(order_repo)
    order = await use_case.execute(
        UpdateOrderStatusInput(
            order_id=order_id,
            status=request.status,
            user_id=user_id,
        )
    )
    return OrderResponse.from_entity(order)
