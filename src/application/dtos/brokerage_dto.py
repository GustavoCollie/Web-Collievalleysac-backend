from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class CreateBrokerageInput:
    user_id: UUID
    origin_country: str
    dest_country: str
    product_type: str
    volume_kg: float
    certifications: list[str] = field(default_factory=list)
    notes: str = ""
