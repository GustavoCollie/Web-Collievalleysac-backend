from datetime import date

from domain.entities.order import Order, OrderItem
from domain.exceptions.order import InvalidOrder
from domain.ports.repositories.order_repository import OrderRepository
from domain.ports.repositories.product_repository import ProductRepository
from application.dtos.order_dto import CreateOrderInput


class CreateOrderUseCase:
    def __init__(
        self,
        order_repo: OrderRepository,
        product_repo: ProductRepository,
    ):
        self._order_repo = order_repo
        self._product_repo = product_repo

    async def execute(self, input: CreateOrderInput) -> Order:
        order_items: list[OrderItem] = []

        for item_input in input.items:
            product = await self._product_repo.find_by_id(item_input.product_id)
            if not product:
                raise InvalidOrder(f"Producto {item_input.product_id} no encontrado")
            if not product.is_available:
                raise InvalidOrder(f"Producto '{product.name}' no está disponible")

            order_items.append(
                OrderItem(
                    product_id=product.id,
                    quantity_kg=item_input.quantity_kg,
                    quality_grade=item_input.quality_grade,
                    unit_price=product.price_per_kg,
                )
            )

        delivery = None
        if input.delivery_date:
            delivery = date.fromisoformat(input.delivery_date)

        order = Order(
            user_id=input.user_id,
            items=order_items,
            delivery_date=delivery,
            shipping_address=input.shipping_address,
            notes=input.notes,
        )

        return await self._order_repo.save(order)
