from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.middleware.rbac_middleware import require_role
from api.schemas.product_schemas import (
    CreateProductRequest,
    ProductListResponse,
    ProductResponse,
)
from application.dtos.product_dto import CreateProductInput
from application.use_cases.products.list_products import ListProductsUseCase
from application.use_cases.products.manage_product import CreateProductUseCase, DeleteProductUseCase
from infrastructure.persistence.database import get_session
from infrastructure.persistence.repositories.pg_product_repository import PgProductRepository

router = APIRouter(prefix="/products", tags=["products"])


def _get_repo(session: AsyncSession = Depends(get_session)):
    return PgProductRepository(session)


@router.get("", response_model=ProductListResponse)
async def list_products(
    month: int | None = Query(None, ge=1, le=12, description="Filtrar por mes de temporada"),
    repo=Depends(_get_repo),
):
    use_case = ListProductsUseCase(repo)
    products = await use_case.execute(month=month)
    return ProductListResponse(
        products=[ProductResponse.from_entity(p) for p in products],
        total=len(products),
    )


@router.post("", response_model=ProductResponse, status_code=201)
async def create_product(
    request: CreateProductRequest,
    _user=Depends(require_role("admin")),
    repo=Depends(_get_repo),
):
    use_case = CreateProductUseCase(repo)
    product = await use_case.execute(
        CreateProductInput(
            name=request.name,
            slug=request.slug,
            category=request.category,
            price_per_kg=request.price_per_kg,
            description=request.description,
            image_url=request.image_url,
            currency=request.currency,
            season_start=request.season_start,
            season_end=request.season_end,
            is_available=request.is_available,
        )
    )
    return ProductResponse.from_entity(product)


@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: UUID,
    _user=Depends(require_role("admin")),
    repo=Depends(_get_repo),
):
    use_case = DeleteProductUseCase(repo)
    await use_case.execute(product_id)
