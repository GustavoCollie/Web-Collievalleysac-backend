from typing import Any
from uuid import UUID

import httpx

from domain.ports.services.collie_app_gateway import CollieAppGateway
from infrastructure.config.settings import settings


class CollieAppClient(CollieAppGateway):
    """HTTP adapter for the external Collie App IA system.

    If Collie App is unavailable, methods return graceful fallbacks
    so the dashboard degrades without crashing.
    """

    def __init__(self):
        self._base_url = settings.collie_app_base_url
        self._client_id = settings.collie_app_client_id
        self._client_secret = settings.collie_app_client_secret

    async def exchange_token(self, user_id: UUID) -> str:
        """Exchange internal token for Collie App SSO token via OAuth2."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self._base_url}/oauth/token",
                    json={
                        "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
                        "client_id": self._client_id,
                        "client_secret": self._client_secret,
                        "subject_token": str(user_id),
                        "subject_token_type": "urn:collie:user_id",
                    },
                )
                response.raise_for_status()
                data = response.json()
                return data.get("access_token", "")
        except (httpx.HTTPError, KeyError):
            return ""

    async def get_ai_metrics(self, external_user_id: str) -> dict[str, Any]:
        """Fetch AI-generated metrics from Collie App."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self._base_url}/api/v1/users/{external_user_id}/metrics",
                    headers={"X-Client-Id": self._client_id},
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError:
            # Return mock data when external service is unavailable
            return {
                "status": "unavailable",
                "crop_yield": {
                    "current": 12.5,
                    "previous": 11.8,
                    "unit": "ton/ha",
                    "trend": "+5.9%",
                },
                "export_forecast": {
                    "next_month_tons": 45.2,
                    "next_quarter_tons": 128.7,
                    "confidence": 0.85,
                },
                "alerts": [
                    {"type": "weather", "message": "Posible helada en zona sur esta semana", "severity": "high"},
                    {"type": "market", "message": "Precio FOB de palta subió 3% esta semana", "severity": "low"},
                ],
                "quality_score": 92,
            }

    async def sync_user_data(self, external_user_id: str) -> dict[str, Any]:
        """Sync basic user data from Collie App."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self._base_url}/api/v1/users/{external_user_id}/profile",
                    headers={"X-Client-Id": self._client_id},
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError:
            return {"status": "unavailable", "synced": False}
