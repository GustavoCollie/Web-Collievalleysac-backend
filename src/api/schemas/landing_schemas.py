from typing import Any

from pydantic import BaseModel, Field


class LandingSectionResponse(BaseModel):
    id: str
    section_key: str
    title: str
    subtitle: str
    content: dict[str, Any]
    display_order: int
    is_visible: bool
    created_at: str

    @classmethod
    def from_entity(cls, section) -> "LandingSectionResponse":
        return cls(
            id=str(section.id),
            section_key=section.section_key,
            title=section.title,
            subtitle=section.subtitle,
            content=section.content,
            display_order=section.display_order,
            is_visible=section.is_visible,
            created_at=section.created_at.isoformat(),
        )


class CreateSectionRequest(BaseModel):
    section_key: str = Field(min_length=2, max_length=50)
    title: str = Field(max_length=200)
    subtitle: str = ""
    content: dict[str, Any] = {}
    display_order: int = 0
    is_visible: bool = True


class UpdateSectionRequest(BaseModel):
    title: str | None = None
    subtitle: str | None = None
    content: dict[str, Any] | None = None
    display_order: int | None = None
    is_visible: bool | None = None


class LandingSectionsListResponse(BaseModel):
    sections: list[LandingSectionResponse]
