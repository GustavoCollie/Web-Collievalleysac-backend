from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateAdvisoryInput:
    user_id: UUID
    crop_type: str
    problem_description: str
    preferred_date: str | None = None
    urgency: str = "medium"
