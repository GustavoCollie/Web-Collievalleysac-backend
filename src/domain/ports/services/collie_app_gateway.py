from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class CollieAppGateway(ABC):
    @abstractmethod
    async def exchange_token(self, user_id: UUID) -> str:
        """Exchange internal token for Collie App SSO token."""
        ...

    @abstractmethod
    async def get_ai_metrics(self, external_user_id: str) -> dict[str, Any]:
        """Fetch AI metrics from Collie App."""
        ...

    @abstractmethod
    async def sync_user_data(self, external_user_id: str) -> dict[str, Any]:
        """Sync basic user data from Collie App."""
        ...
