import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from domain.entities.brokerage import BrokerageRequest, BrokerageStatus
from application.dtos.brokerage_dto import CreateBrokerageInput
from application.use_cases.brokerage.create_brokerage_request import CreateBrokerageRequestUseCase
from application.use_cases.brokerage.list_brokerage_requests import ListBrokerageRequestsUseCase


@pytest.fixture
def mock_brokerage_repo():
    return AsyncMock()


class TestCreateBrokerageRequest:
    @pytest.mark.asyncio
    async def test_create_success(self, mock_brokerage_repo):
        user_id = uuid4()
        mock_brokerage_repo.save.return_value = BrokerageRequest(
            user_id=user_id,
            origin_country="Peru",
            dest_country="USA",
            product_type="Palta Hass",
            volume_kg=5000.0,
            certifications=["GlobalGAP"],
        )

        use_case = CreateBrokerageRequestUseCase(mock_brokerage_repo)
        result = await use_case.execute(
            CreateBrokerageInput(
                user_id=user_id,
                origin_country="Peru",
                dest_country="USA",
                product_type="Palta Hass",
                volume_kg=5000.0,
                certifications=["GlobalGAP"],
            )
        )

        assert result.origin_country == "Peru"
        assert result.dest_country == "USA"
        assert result.status == BrokerageStatus.REQUESTED
        assert "GlobalGAP" in result.certifications
        mock_brokerage_repo.save.assert_called_once()


class TestListBrokerageRequests:
    @pytest.mark.asyncio
    async def test_list_by_user(self, mock_brokerage_repo):
        user_id = uuid4()
        mock_brokerage_repo.find_by_user.return_value = [
            BrokerageRequest(
                user_id=user_id,
                origin_country="Peru",
                dest_country="USA",
                product_type="Palta",
                volume_kg=1000,
            ),
        ]

        use_case = ListBrokerageRequestsUseCase(mock_brokerage_repo)
        result = await use_case.execute(user_id)

        assert len(result) == 1
        mock_brokerage_repo.find_by_user.assert_called_once_with(user_id)
