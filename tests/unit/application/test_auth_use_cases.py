import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from domain.entities.user import User, Role
from domain.exceptions.auth import InvalidCredentials
from domain.exceptions.base import DuplicateEntity
from application.dtos.auth_dto import LoginInput, RegisterInput, RefreshInput
from application.use_cases.auth.register_user import RegisterUserUseCase
from application.use_cases.auth.login_user import LoginUserUseCase
from application.use_cases.auth.refresh_token import RefreshTokenUseCase
from application.use_cases.auth.get_profile import GetProfileUseCase


@pytest.fixture
def mock_user_repo():
    repo = AsyncMock()
    return repo


@pytest.fixture
def mock_auth_service():
    service = MagicMock()
    service.hash_password.return_value = "hashed_password"
    service.verify_password.return_value = True
    service.create_access_token.return_value = "access_token_123"
    service.create_refresh_token.return_value = "refresh_token_123"
    service.decode_token.return_value = {"sub": str(uuid4()), "role": "admin", "type": "access"}
    return service


class TestRegisterUser:
    @pytest.mark.asyncio
    async def test_register_success(self, mock_user_repo, mock_auth_service):
        mock_user_repo.find_by_email.return_value = None
        mock_user_repo.save.return_value = User(
            email="test@example.com",
            full_name="Test User",
            role=Role.IMPORTADOR,
            hashed_password="hashed_password",
        )

        use_case = RegisterUserUseCase(mock_user_repo, mock_auth_service)
        result = await use_case.execute(
            RegisterInput(
                email="test@example.com",
                password="password123",
                full_name="Test User",
                role=Role.IMPORTADOR,
            )
        )

        assert result.email == "test@example.com"
        assert result.role == Role.IMPORTADOR
        mock_auth_service.hash_password.assert_called_once_with("password123")
        mock_user_repo.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, mock_user_repo, mock_auth_service):
        mock_user_repo.find_by_email.return_value = User(
            email="existing@example.com",
            full_name="Existing",
            role=Role.IMPORTADOR,
        )

        use_case = RegisterUserUseCase(mock_user_repo, mock_auth_service)
        with pytest.raises(DuplicateEntity):
            await use_case.execute(
                RegisterInput(
                    email="existing@example.com",
                    password="password123",
                    full_name="New User",
                    role=Role.IMPORTADOR,
                )
            )

    @pytest.mark.asyncio
    async def test_register_invalid_email(self, mock_user_repo, mock_auth_service):
        use_case = RegisterUserUseCase(mock_user_repo, mock_auth_service)
        with pytest.raises(Exception):
            await use_case.execute(
                RegisterInput(
                    email="not-valid-email",
                    password="password123",
                    full_name="Test",
                    role=Role.IMPORTADOR,
                )
            )


class TestLoginUser:
    @pytest.mark.asyncio
    async def test_login_success(self, mock_user_repo, mock_auth_service):
        user = User(
            id=uuid4(),
            email="test@example.com",
            full_name="Test",
            role=Role.IMPORTADOR,
            hashed_password="hashed_password",
            is_active=True,
        )
        mock_user_repo.find_by_email.return_value = user

        use_case = LoginUserUseCase(mock_user_repo, mock_auth_service)
        result = await use_case.execute(
            LoginInput(email="test@example.com", password="correct_pass")
        )

        assert result.access_token == "access_token_123"
        assert result.refresh_token == "refresh_token_123"
        assert result.token_type == "bearer"

    @pytest.mark.asyncio
    async def test_login_user_not_found(self, mock_user_repo, mock_auth_service):
        mock_user_repo.find_by_email.return_value = None

        use_case = LoginUserUseCase(mock_user_repo, mock_auth_service)
        with pytest.raises(InvalidCredentials):
            await use_case.execute(
                LoginInput(email="nonexistent@example.com", password="pass")
            )

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, mock_user_repo, mock_auth_service):
        user = User(
            email="test@example.com",
            full_name="Test",
            role=Role.IMPORTADOR,
            hashed_password="hashed",
            is_active=True,
        )
        mock_user_repo.find_by_email.return_value = user
        mock_auth_service.verify_password.return_value = False

        use_case = LoginUserUseCase(mock_user_repo, mock_auth_service)
        with pytest.raises(InvalidCredentials):
            await use_case.execute(
                LoginInput(email="test@example.com", password="wrong_pass")
            )

    @pytest.mark.asyncio
    async def test_login_inactive_user(self, mock_user_repo, mock_auth_service):
        user = User(
            email="test@example.com",
            full_name="Test",
            role=Role.IMPORTADOR,
            hashed_password="hashed",
            is_active=False,
        )
        mock_user_repo.find_by_email.return_value = user

        use_case = LoginUserUseCase(mock_user_repo, mock_auth_service)
        with pytest.raises(InvalidCredentials):
            await use_case.execute(
                LoginInput(email="test@example.com", password="pass")
            )


class TestRefreshToken:
    @pytest.mark.asyncio
    async def test_refresh_success(self, mock_user_repo, mock_auth_service):
        user_id = uuid4()
        user = User(
            id=user_id,
            email="test@example.com",
            full_name="Test",
            role=Role.IMPORTADOR,
            is_active=True,
        )
        mock_auth_service.decode_token.return_value = {
            "sub": str(user_id),
            "type": "refresh",
        }
        mock_user_repo.find_by_id.return_value = user

        use_case = RefreshTokenUseCase(mock_user_repo, mock_auth_service)
        result = await use_case.execute(RefreshInput(refresh_token="valid_refresh"))

        assert result.access_token == "access_token_123"
        assert result.refresh_token == "refresh_token_123"

    @pytest.mark.asyncio
    async def test_refresh_with_access_token_fails(self, mock_user_repo, mock_auth_service):
        mock_auth_service.decode_token.return_value = {
            "sub": str(uuid4()),
            "type": "access",
        }

        use_case = RefreshTokenUseCase(mock_user_repo, mock_auth_service)
        with pytest.raises(InvalidCredentials):
            await use_case.execute(RefreshInput(refresh_token="access_token"))


class TestGetProfile:
    @pytest.mark.asyncio
    async def test_get_profile_success(self, mock_user_repo):
        user_id = uuid4()
        user = User(
            id=user_id,
            email="test@example.com",
            full_name="Test",
            role=Role.ADMIN,
        )
        mock_user_repo.find_by_id.return_value = user

        use_case = GetProfileUseCase(mock_user_repo)
        result = await use_case.execute(user_id)

        assert result.email == "test@example.com"
        assert result.role == Role.ADMIN

    @pytest.mark.asyncio
    async def test_get_profile_not_found(self, mock_user_repo):
        mock_user_repo.find_by_id.return_value = None

        use_case = GetProfileUseCase(mock_user_repo)
        with pytest.raises(Exception):
            await use_case.execute(uuid4())
