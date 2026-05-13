from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class OrderItemInput:
    product_id: UUID
    quantity_kg: float
    quality_grade: str


@dataclass
class CreateOrderInput:
    user_id: UUID
    items: list[OrderItemInput]
    delivery_date: str | None = None
    shipping_address: str = ""
    notes: str = ""


@dataclass
class UpdateOrderStatusInput:
    order_id: UUID
    status: str
    user_id: UUID  # for ownership verification
