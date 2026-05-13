from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class BrokerageStatus(str, Enum):
    REQUESTED = "requested"
    QUOTED = "quoted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class BrokerageRequest:
    user_id: UUID
    origin_country: str
    dest_country: str
    product_type: str
    volume_kg: float
    id: UUID = field(default_factory=uuid4)
    certifications: list[str] = field(default_factory=list)
    status: BrokerageStatus = BrokerageStatus.REQUESTED
    quoted_price: float | None = None
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None
