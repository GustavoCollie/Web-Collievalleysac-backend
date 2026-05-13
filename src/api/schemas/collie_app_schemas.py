from typing import Any

from pydantic import BaseModel


class CollieMetricsResponse(BaseModel):
    status: str
    crop_yield: dict[str, Any] | None = None
    export_forecast: dict[str, Any] | None = None
    alerts: list[dict[str, Any]] = []
    quality_score: int | None = None


class CollieSSOResponse(BaseModel):
    redirect_url: str
    token: str


class CollieSyncResponse(BaseModel):
    status: str
    synced: bool
