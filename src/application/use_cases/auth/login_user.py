from domain.exceptions.auth import InvalidCredentials
from domain.ports.repositories.user_repository import UserRepository
from domain.ports.services.auth_service import AuthService
from application.dtos.auth_dto import AuthTokensOutput, LoginInput


class LoginUserUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        auth_service: AuthService,
    ):
        self._user_repo = user_repo
        self._auth_service = auth_service

    async def execute(self, input: LoginInput) -> AuthTokensOutput:
        user = await self._user_repo.find_by_email(input.email.lower().strip())
        if not user:
            raise InvalidCredentials()

        if not user.is_active:
            raise InvalidCredentials()

        if not self._auth_service.verify_password(input.password, user.hashed_password):
            raise InvalidCredentials()

        access_token = self._auth_service.create_access_token(user.id, user.role.value)
        refresh_token = self._auth_service.create_refresh_token(user.id)

        return AuthTokensOutput(
            access_token=access_token,
            refresh_token=refresh_token,
        )
