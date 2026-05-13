from pydantic import BaseModel, Field


class OrderItemRequest(BaseModel):
    product_id: str
    quantity_kg: float = Field(gt=0)
    quality_grade: str = Field(default="Standard", max_length=20)


class CreateOrderRequest(BaseModel):
    items: list[OrderItemRequest] = Field(min_length=1)
    delivery_date: str | None = None
    shipping_address: str = ""
    notes: str = ""


class UpdateOrderStatusRequest(BaseModel):
    status: str


class OrderItemResponse(BaseModel):
    id: str
    product_id: str
    quantity_kg: float
    quality_grade: str
    unit_price: float
    subtotal: float


class OrderResponse(BaseModel):
    id: str
    user_id: str
    status: str
    total_amount: float
    currency: str
    delivery_date: str | None
    shipping_address: str
    notes: str
    items: list[OrderItemResponse]
    created_at: str

    @classmethod
    def from_entity(cls, order) -> "OrderResponse":
        return cls(
            id=str(order.id),
            user_id=str(order.user_id),
            status=order.status.value,
            total_amount=order.total_amount,
            currency=order.currency,
            delivery_date=order.delivery_date.isoformat() if order.delivery_date else None,
            shipping_address=order.shipping_address,
            notes=order.notes,
            items=[
                OrderItemResponse(
                    id=str(item.id),
                    product_id=str(item.product_id),
                    quantity_kg=item.quantity_kg,
                    quality_grade=item.quality_grade,
                    unit_price=item.unit_price,
                    subtotal=item.subtotal,
                )
                for item in order.items
            ],
            created_at=order.created_at.isoformat(),
        )


class OrderListResponse(BaseModel):
    orders: list[OrderResponse]
    total: int
