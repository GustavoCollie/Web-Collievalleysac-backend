from uuid import UUID

from domain.entities.advisory import AdvisoryRequest
from domain.ports.repositories.advisory_repository import AdvisoryRepository


class ListAdvisoriesUseCase:
    def __init__(self, advisory_repo: AdvisoryRepository):
        self._advisory_repo = advisory_repo

    async def execute(self, user_id: UUID) -> list[AdvisoryRequest]:
        return await self._advisory_repo.find_by_user(user_id)
