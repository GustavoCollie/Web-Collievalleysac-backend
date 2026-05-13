from typing import Any

from domain.ports.services.collie_app_gateway import CollieAppGateway


class GetAIMetricsUseCase:
    def __init__(self, collie_gateway: CollieAppGateway):
        self._collie_gateway = collie_gateway

    async def execute(self, external_user_id: str) -> dict[str, Any]:
        return await self._collie_gateway.get_ai_metrics(external_user_id)
