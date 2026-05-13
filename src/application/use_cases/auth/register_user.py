from domain.entities.user import User
from domain.exceptions.base import DuplicateEntity
from domain.ports.repositories.user_repository import UserRepository
from domain.ports.services.auth_service import AuthService
from domain.value_objects.email import Email
from application.dtos.auth_dto import RegisterInput


class RegisterUserUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        auth_service: AuthService,
    ):
        self._user_repo = user_repo
        self._auth_service = auth_service

    async def execute(self, input: RegisterInput) -> User:
        # Validate email format via value object
        email_vo = Email(input.email)

        # Check for duplicates
        existing = await self._user_repo.find_by_email(email_vo.value)
        if existing:
            raise DuplicateEntity("Usuario", f"email '{email_vo.value}'")

        hashed = self._auth_service.hash_password(input.password)

        user = User(
            email=email_vo.value,
            hashed_password=hashed,
            full_name=input.full_name,
            phone=input.phone,
            role=input.role,
        )

        return await self._user_repo.save(user)
