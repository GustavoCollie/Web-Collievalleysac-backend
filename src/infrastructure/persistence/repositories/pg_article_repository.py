from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.advisory import TechnicalArticle
from domain.ports.repositories.advisory_repository import ArticleRepository
from infrastructure.persistence.models.advisory_model import TechnicalArticleORM


class PgArticleRepository(ArticleRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    def _to_domain(self, orm: TechnicalArticleORM) -> TechnicalArticle:
        return TechnicalArticle(
            id=orm.id,
            title=orm.title,
            slug=orm.slug,
            content=orm.content,
            crop_tags=orm.crop_tags or [],
            author=orm.author or "",
            published_at=orm.published_at,
            created_at=orm.created_at,
        )

    async def find_all(self, crop_tags: list[str] | None = None) -> list[TechnicalArticle]:
        stmt = select(TechnicalArticleORM).order_by(TechnicalArticleORM.created_at.desc())
        if crop_tags:
            # Filter articles that have any of the provided crop tags
            stmt = stmt.where(TechnicalArticleORM.crop_tags.overlap(crop_tags))
        result = await self._session.execute(stmt)
        return [self._to_domain(orm) for orm in result.scalars().all()]

    async def find_by_slug(self, slug: str) -> TechnicalArticle | None:
        stmt = select(TechnicalArticleORM).where(TechnicalArticleORM.slug == slug)
        result = await self._session.execute(stmt)
        orm = result.scalar_one_or_none()
        return self._to_domain(orm) if orm else None

    async def save(self, article: TechnicalArticle) -> TechnicalArticle:
        orm = TechnicalArticleORM(
            id=article.id,
            title=article.title,
            slug=article.slug,
            content=article.content,
            crop_tags=article.crop_tags,
            author=article.author,
            published_at=article.published_at,
        )
        self._session.add(orm)
        await self._session.commit()
        await self._session.refresh(orm)
        return self._to_domain(orm)
