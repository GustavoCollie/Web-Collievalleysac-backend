from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from uuid import UUID, uuid4


class Urgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AdvisoryStatus(str, Enum):
    REQUESTED = "requested"
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class AdvisoryRequest:
    user_id: UUID
    crop_type: str
    problem_description: str
    id: UUID = field(default_factory=uuid4)
    preferred_date: date | None = None
    urgency: Urgency = Urgency.MEDIUM
    status: AdvisoryStatus = AdvisoryStatus.REQUESTED
    advisor_notes: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None


@dataclass
class TechnicalArticle:
    title: str
    slug: str
    content: str
    id: UUID = field(default_factory=uuid4)
    crop_tags: list[str] = field(default_factory=list)
    author: str = ""
    published_at: datetime | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
