from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Product:
    name: str
    slug: str
    category: str
    price_per_kg: float
    id: UUID = field(default_factory=uuid4)
    description: str = ""
    image_url: str = ""
    currency: str = "USD"
    season_start: int = 1
    season_end: int = 12
    is_available: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None
