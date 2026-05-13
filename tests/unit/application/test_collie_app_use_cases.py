import pytest
from unittest.mock import AsyncMock

from application.use_cases.collie_app.get_ai_metrics import GetAIMetricsUseCase
from application.use_cases.collie_app.sync_collie_data import SyncCollieDataUseCase


@pytest.fixture
def mock_gateway():
    return AsyncMock()


class TestGetAIMetrics:
    @pytest.mark.asyncio
    async def test_get_metrics(self, mock_gateway):
        mock_gateway.get_ai_metrics.return_value = {
            "status": "ok",
            "crop_yield": {"current": 12.5, "previous": 11.8, "unit": "ton/ha", "trend": "+5.9%"},
            "quality_score": 92,
            "alerts": [],
        }

        use_case = GetAIMetricsUseCase(mock_gateway)
        result = await use_case.execute("ext-123")

        assert result["status"] == "ok"
        assert result["quality_score"] == 92
        mock_gateway.get_ai_metrics.assert_called_once_with("ext-123")

    @pytest.mark.asyncio
    async def test_get_metrics_unavailable(self, mock_gateway):
        mock_gateway.get_ai_metrics.return_value = {"status": "unavailable"}

        use_case = GetAIMetricsUseCase(mock_gateway)
        result = await use_case.execute("ext-123")

        assert result["status"] == "unavailable"


class TestSyncCollieData:
    @pytest.mark.asyncio
    async def test_sync_success(self, mock_gateway):
        mock_gateway.sync_user_data.return_value = {"status": "ok", "synced": True}

        use_case = SyncCollieDataUseCase(mock_gateway)
        result = await use_case.execute("ext-456")

        assert result["synced"] is True

    @pytest.mark.asyncio
    async def test_sync_unavailable(self, mock_gateway):
        mock_gateway.sync_user_data.return_value = {"status": "unavailable", "synced": False}

        use_case = SyncCollieDataUseCase(mock_gateway)
        result = await use_case.execute("ext-456")

        assert result["synced"] is False
