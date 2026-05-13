from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.middleware.rbac_middleware import require_role
from api.schemas.collie_app_schemas import CollieMetricsResponse, CollieSSOResponse, CollieSyncResponse
from application.use_cases.collie_app.get_ai_metrics import GetAIMetricsUseCase
from application.use_cases.collie_app.sync_collie_data import SyncCollieDataUseCase
from infrastructure.external.collie_app_client import CollieAppClient
from infrastructure.persistence.database import get_session
from infrastructure.persistence.models.profile_models import CollieAppProfileORM
from infrastructure.config.settings import settings

router = APIRouter(prefix="/collie-app", tags=["collie-app"])


def _get_gateway():
    return CollieAppClient()


@router.get("/metrics", response_model=CollieMetricsResponse)
async def get_ai_metrics(
    user=Depends(require_role("exportador_collie")),
    session: AsyncSession = Depends(get_session),
    gateway=Depends(_get_gateway),
):
    user_id, _ = user
    # Look up Collie App external ID from profile
    profile = await session.get(CollieAppProfileORM, user_id)
    external_id = profile.collie_external_id if profile else str(user_id)

    use_case = GetAIMetricsUseCase(gateway)
    metrics = await use_case.execute(external_id)
    return CollieMetricsResponse(**metrics)


@router.get("/redirect", response_model=CollieSSOResponse)
async def get_sso_redirect(
    user=Depends(require_role("exportador_collie")),
    gateway=Depends(_get_gateway),
):
    user_id, _ = user
    token = await gateway.exchange_token(user_id)
    base_url = settings.collie_app_base_url
    redirect_url = f"{base_url}/sso?token={token}" if token else f"{base_url}/login"
    return CollieSSOResponse(redirect_url=redirect_url, token=token)


@router.post("/sync", response_model=CollieSyncResponse)
async def sync_data(
    user=Depends(require_role("exportador_collie")),
    session: AsyncSession = Depends(get_session),
    gateway=Depends(_get_gateway),
):
    user_id, _ = user
    profile = await session.get(CollieAppProfileORM, user_id)
    external_id = profile.collie_external_id if profile else str(user_id)

    use_case = SyncCollieDataUseCase(gateway)
    result = await use_case.execute(external_id)
    return CollieSyncResponse(
        status=result.get("status", "unknown"),
        synced=result.get("synced", False),
    )
