import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from domain.entities.advisory import AdvisoryRequest, AdvisoryStatus, TechnicalArticle, Urgency
from application.dtos.advisory_dto import CreateAdvisoryInput
from application.use_cases.advisory.request_advisory import RequestAdvisoryUseCase
from application.use_cases.advisory.list_advisories import ListAdvisoriesUseCase
from application.use_cases.advisory.list_articles import ListArticlesUseCase


@pytest.fixture
def mock_advisory_repo():
    return AsyncMock()


@pytest.fixture
def mock_article_repo():
    return AsyncMock()


class TestRequestAdvisory:
    @pytest.mark.asyncio
    async def test_create_advisory(self, mock_advisory_repo):
        user_id = uuid4()
        mock_advisory_repo.save.return_value = AdvisoryRequest(
            user_id=user_id,
            crop_type="Palta",
            problem_description="Hojas amarillentas en sector norte",
            urgency=Urgency.HIGH,
        )

        use_case = RequestAdvisoryUseCase(mock_advisory_repo)
        result = await use_case.execute(
            CreateAdvisoryInput(
                user_id=user_id,
                crop_type="Palta",
                problem_description="Hojas amarillentas en sector norte",
                urgency="high",
            )
        )

        assert result.crop_type == "Palta"
        assert result.status == AdvisoryStatus.REQUESTED
        mock_advisory_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_with_date(self, mock_advisory_repo):
        user_id = uuid4()
        mock_advisory_repo.save.return_value = AdvisoryRequest(
            user_id=user_id,
            crop_type="Mandarina",
            problem_description="Mosca de la fruta detectada",
        )

        use_case = RequestAdvisoryUseCase(mock_advisory_repo)
        result = await use_case.execute(
            CreateAdvisoryInput(
                user_id=user_id,
                crop_type="Mandarina",
                problem_description="Mosca de la fruta detectada",
                preferred_date="2026-06-15",
            )
        )

        assert result.crop_type == "Mandarina"


class TestListAdvisories:
    @pytest.mark.asyncio
    async def test_list_by_user(self, mock_advisory_repo):
        user_id = uuid4()
        mock_advisory_repo.find_by_user.return_value = []

        use_case = ListAdvisoriesUseCase(mock_advisory_repo)
        result = await use_case.execute(user_id)

        assert result == []
        mock_advisory_repo.find_by_user.assert_called_once_with(user_id)


class TestListArticles:
    @pytest.mark.asyncio
    async def test_list_all(self, mock_article_repo):
        mock_article_repo.find_all.return_value = [
            TechnicalArticle(title="Riego eficiente", slug="riego", content="..."),
        ]

        use_case = ListArticlesUseCase(mock_article_repo)
        result = await use_case.execute()

        assert len(result) == 1
        mock_article_repo.find_all.assert_called_once_with(crop_tags=None)

    @pytest.mark.asyncio
    async def test_list_filtered(self, mock_article_repo):
        mock_article_repo.find_all.return_value = []

        use_case = ListArticlesUseCase(mock_article_repo)
        result = await use_case.execute(crop_tags=["palta"])

        assert result == []
        mock_article_repo.find_all.assert_called_once_with(crop_tags=["palta"])
