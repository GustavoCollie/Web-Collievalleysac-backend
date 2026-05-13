from pydantic import BaseModel, Field


class CreateBrokerageRequest(BaseModel):
    origin_country: str = Field(min_length=2, max_length=100)
    dest_country: str = Field(min_length=2, max_length=100)
    product_type: str = Field(max_length=100)
    volume_kg: float = Field(gt=0)
    certifications: list[str] = []
    notes: str = ""


class BrokerageResponse(BaseModel):
    id: str
    user_id: str
    origin_country: str
    dest_country: str
    product_type: str
    volume_kg: float
    certifications: list[str]
    status: str
    quoted_price: float | None
    notes: str
    created_at: str

    @classmethod
    def from_entity(cls, req) -> "BrokerageResponse":
        return cls(
            id=str(req.id),
            user_id=str(req.user_id),
            origin_country=req.origin_country,
            dest_country=req.dest_country,
            product_type=req.product_type,
            volume_kg=req.volume_kg,
            certifications=req.certifications,
            status=req.status.value,
            quoted_price=req.quoted_price,
            notes=req.notes,
            created_at=req.created_at.isoformat(),
        )


class BrokerageListResponse(BaseModel):
    requests: list[BrokerageResponse]
    total: int
