from dataclasses import dataclass, field
from typing import Any
from uuid import UUID


@dataclass
class CreateSectionInput:
    section_key: str
    title: str
    subtitle: str = ""
    content: dict[str, Any] = field(default_factory=dict)
    display_order: int = 0
    is_visible: bool = True
    updated_by: UUID | None = None


@dataclass
class UpdateSectionInput:
    section_key: str
    title: str | None = None
    subtitle: str | None = None
    content: dict[str, Any] | None = None
    display_order: int | None = None
    is_visible: bool | None = None
    updated_by: UUID | None = None
