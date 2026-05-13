from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.middleware.rbac_middleware import require_role
from api.schemas.advisory_schemas import (
    AdvisoryListResponse,
    AdvisoryResponse,
    ArticleListResponse,
    ArticleResponse,
    CreateAdvisoryRequest,
)
from application.dtos.advisory_dto import CreateAdvisoryInput
from application.use_cases.advisory.list_advisories import ListAdvisoriesUseCase
from application.use_cases.advisory.list_articles import ListArticlesUseCase
from application.use_cases.advisory.request_advisory import RequestAdvisoryUseCase
from infrastructure.persistence.database import get_session
from infrastructure.persistence.repositories.pg_advisory_repository import PgAdvisoryRepository
from infrastructure.persistence.repositories.pg_article_repository import PgArticleRepository

router = APIRouter(tags=["advisory"])


def _get_advisory_repo(session: AsyncSession = Depends(get_session)):
    return PgAdvisoryRepository(session)


def _get_article_repo(session: AsyncSession = Depends(get_session)):
    return PgArticleRepository(session)


# --- Advisory Requests ---


@router.post("/advisories", response_model=AdvisoryResponse, status_code=201)
async def create_advisory(
    request: CreateAdvisoryRequest,
    user=Depends(require_role("agricultor")),
    repo=Depends(_get_advisory_repo),
):
    user_id, _ = user
    use_case = RequestAdvisoryUseCase(repo)
    result = await use_case.execute(
        CreateAdvisoryInput(
            user_id=user_id,
            crop_type=request.crop_type,
            problem_description=request.problem_description,
            preferred_date=request.preferred_date,
            urgency=request.urgency,
        )
    )
    return AdvisoryResponse.from_entity(result)


@router.get("/advisories", response_model=AdvisoryListResponse)
async def list_my_advisories(
    user=Depends(require_role("agricultor")),
    repo=Depends(_get_advisory_repo),
):
    user_id, _ = user
    use_case = ListAdvisoriesUseCase(repo)
    advisories = await use_case.execute(user_id)
    return AdvisoryListResponse(
        advisories=[AdvisoryResponse.from_entity(a) for a in advisories],
        total=len(advisories),
    )


# --- Technical Articles ---


@router.get("/articles", response_model=ArticleListResponse)
async def list_articles(
    crop_tags: str | None = Query(None, description="Comma-separated crop tags to filter"),
    user=Depends(require_role("agricultor")),
    repo=Depends(_get_article_repo),
):
    tags = [t.strip() for t in crop_tags.split(",")] if crop_tags else None
    use_case = ListArticlesUseCase(repo)
    articles = await use_case.execute(crop_tags=tags)
    return ArticleListResponse(
        articles=[ArticleResponse.from_entity(a) for a in articles],
        total=len(articles),
    )


@router.get("/articles/{slug}", response_model=ArticleResponse)
async def get_article(
    slug: str,
    user=Depends(require_role("agricultor")),
    repo=Depends(_get_article_repo),
):
    from domain.exceptions.base import EntityNotFound

    article = await repo.find_by_slug(slug)
    if not article:
        raise EntityNotFound("Artículo", slug)
    return ArticleResponse.from_entity(article)
