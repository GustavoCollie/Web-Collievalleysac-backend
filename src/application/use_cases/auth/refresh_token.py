from uuid import UUID

from domain.exceptions.auth import InvalidCredentials, TokenExpired
from domain.ports.repositories.user_repository import UserRepository
from domain.ports.services.auth_service import AuthService
from application.dtos.auth_dto import AuthTokensOutput, RefreshInput


class RefreshTokenUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        auth_service: AuthService,
    ):
        self._user_repo = user_repo
        self._auth_service = auth_service

    async def execute(self, input: RefreshInput) -> AuthTokensOutput:
        payload = self._auth_service.decode_token(input.refresh_token)

        if payload.get("type") != "refresh":
            raise InvalidCredentials()

        user_id = UUID(payload["sub"])
        user = await self._user_repo.find_by_id(user_id)
        if not user or not user.is_active:
            raise InvalidCredentials()

        access_token = self._auth_service.create_access_token(user.id, user.role.value)
        refresh_token = self._auth_service.create_refresh_token(user.id)

        return AuthTokensOutput(
            access_token=access_token,
            refresh_token=refresh_token,
        )
