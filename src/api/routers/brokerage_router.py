from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.middleware.rbac_middleware import require_role
from api.schemas.brokerage_schemas import (
    BrokerageListResponse,
    BrokerageResponse,
    CreateBrokerageRequest,
)
from application.dtos.brokerage_dto import CreateBrokerageInput
from application.use_cases.brokerage.create_brokerage_request import CreateBrokerageRequestUseCase
from application.use_cases.brokerage.list_brokerage_requests import ListBrokerageRequestsUseCase
from infrastructure.persistence.database import get_session
from infrastructure.persistence.repositories.pg_brokerage_repository import PgBrokerageRepository

router = APIRouter(prefix="/brokerage", tags=["brokerage"])


def _get_repo(session: AsyncSession = Depends(get_session)):
    return PgBrokerageRepository(session)


@router.post("", response_model=BrokerageResponse, status_code=201)
async def create_brokerage_request(
    request: CreateBrokerageRequest,
    user=Depends(require_role("exportador_broker")),
    repo=Depends(_get_repo),
):
    user_id, _ = user
    use_case = CreateBrokerageRequestUseCase(repo)
    result = await use_case.execute(
        CreateBrokerageInput(
            user_id=user_id,
            origin_country=request.origin_country,
            dest_country=request.dest_country,
            product_type=request.product_type,
            volume_kg=request.volume_kg,
            certifications=request.certifications,
            notes=request.notes,
        )
    )
    return BrokerageResponse.from_entity(result)


@router.get("", response_model=BrokerageListResponse)
async def list_my_brokerage_requests(
    user=Depends(require_role("exportador_broker")),
    repo=Depends(_get_repo),
):
    user_id, _ = user
    use_case = ListBrokerageRequestsUseCase(repo)
    requests = await use_case.execute(user_id)
    return BrokerageListResponse(
        requests=[BrokerageResponse.from_entity(r) for r in requests],
        total=len(requests),
    )
