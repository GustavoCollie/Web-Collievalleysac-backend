from pydantic import BaseModel, Field


class CreateAdvisoryRequest(BaseModel):
    crop_type: str = Field(min_length=2, max_length=100)
    problem_description: str = Field(min_length=10)
    preferred_date: str | None = None
    urgency: str = Field(default="medium", pattern="^(low|medium|high)$")


class AdvisoryResponse(BaseModel):
    id: str
    user_id: str
    crop_type: str
    problem_description: str
    preferred_date: str | None
    urgency: str
    status: str
    advisor_notes: str
    created_at: str

    @classmethod
    def from_entity(cls, req) -> "AdvisoryResponse":
        return cls(
            id=str(req.id),
            user_id=str(req.user_id),
            crop_type=req.crop_type,
            problem_description=req.problem_description,
            preferred_date=req.preferred_date.isoformat() if req.preferred_date else None,
            urgency=req.urgency.value,
            status=req.status.value,
            advisor_notes=req.advisor_notes,
            created_at=req.created_at.isoformat(),
        )


class AdvisoryListResponse(BaseModel):
    advisories: list[AdvisoryResponse]
    total: int


class ArticleResponse(BaseModel):
    id: str
    title: str
    slug: str
    content: str
    crop_tags: list[str]
    author: str
    published_at: str | None
    created_at: str

    @classmethod
    def from_entity(cls, article) -> "ArticleResponse":
        return cls(
            id=str(article.id),
            title=article.title,
            slug=article.slug,
            content=article.content,
            crop_tags=article.crop_tags,
            author=article.author,
            published_at=article.published_at.isoformat() if article.published_at else None,
            created_at=article.created_at.isoformat(),
        )


class ArticleListResponse(BaseModel):
    articles: list[ArticleResponse]
    total: int
