from dataclasses import dataclass


@dataclass
class CreateProductInput:
    name: str
    slug: str
    category: str
    price_per_kg: float
    description: str = ""
    image_url: str = ""
    currency: str = "USD"
    season_start: int = 1
    season_end: int = 12
    is_available: bool = True
