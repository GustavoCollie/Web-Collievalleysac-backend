from uuid import UUID

from domain.entities.brokerage import BrokerageRequest
from domain.ports.repositories.brokerage_repository import BrokerageRepository


class ListBrokerageRequestsUseCase:
    def __init__(self, brokerage_repo: BrokerageRepository):
        self._brokerage_repo = brokerage_repo

    async def execute(self, user_id: UUID) -> list[BrokerageRequest]:
        return await self._brokerage_repo.find_by_user(user_id)
