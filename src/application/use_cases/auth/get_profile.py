from uuid import UUID

from domain.entities.user import User
from domain.exceptions.base import EntityNotFound
from domain.ports.repositories.user_repository import UserRepository


class GetProfileUseCase:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def execute(self, user_id: UUID) -> User:
        user = await self._user_repo.find_by_id(user_id)
        if not user:
            raise EntityNotFound("Usuario", str(user_id))
        return user
