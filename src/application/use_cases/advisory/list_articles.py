from domain.entities.advisory import TechnicalArticle
from domain.ports.repositories.advisory_repository import ArticleRepository


class ListArticlesUseCase:
    def __init__(self, article_repo: ArticleRepository):
        self._article_repo = article_repo

    async def execute(self, crop_tags: list[str] | None = None) -> list[TechnicalArticle]:
        return await self._article_repo.find_all(crop_tags=crop_tags)
