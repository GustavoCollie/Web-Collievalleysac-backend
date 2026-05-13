from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass
class LandingSection:
    section_key: str
    title: str
    id: UUID = field(default_factory=uuid4)
    subtitle: str = ""
    content: dict[str, Any] = field(default_factory=dict)
    display_order: int = 0
    is_visible: bool = True
    updated_by: UUID | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None
