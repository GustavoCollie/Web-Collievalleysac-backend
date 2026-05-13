from pydantic import BaseModel, Field


class ProductResponse(BaseModel):
    id: str
    name: str
    slug: str
    description: str
    category: str
    image_url: str
    price_per_kg: float
    currency: str
    season_start: int
    season_end: int
    is_available: bool

    @classmethod
    def from_entity(cls, product) -> "ProductResponse":
        return cls(
            id=str(product.id),
            name=product.name,
            slug=product.slug,
            description=product.description,
            category=product.category,
            image_url=product.image_url,
            price_per_kg=product.price_per_kg,
            currency=product.currency,
            season_start=product.season_start,
            season_end=product.season_end,
            is_available=product.is_available,
        )


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    total: int


class CreateProductRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    slug: str = Field(min_length=2, max_length=100)
    category: str = Field(max_length=50)
    price_per_kg: float = Field(gt=0)
    description: str = ""
    image_url: str = ""
    currency: str = "USD"
    season_start: int = Field(ge=1, le=12, default=1)
    season_end: int = Field(ge=1, le=12, default=12)
    is_available: bool = True
