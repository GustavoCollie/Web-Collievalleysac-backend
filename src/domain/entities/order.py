from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from uuid import UUID, uuid4

from domain.exceptions.order import InvalidOrder


class OrderStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class OrderItem:
    product_id: UUID
    quantity_kg: float
    quality_grade: str
    unit_price: float
    id: UUID = field(default_factory=uuid4)

    @property
    def subtotal(self) -> float:
        return round(self.quantity_kg * self.unit_price, 2)


@dataclass
class Order:
    user_id: UUID
    items: list[OrderItem]
    id: UUID = field(default_factory=uuid4)
    status: OrderStatus = OrderStatus.DRAFT
    currency: str = "USD"
    delivery_date: date | None = None
    shipping_address: str = ""
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.items:
            raise InvalidOrder("Un pedido debe tener al menos un ítem")

    @property
    def total_amount(self) -> float:
        return round(sum(item.subtotal for item in self.items), 2)
