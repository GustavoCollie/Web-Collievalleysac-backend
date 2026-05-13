import pytest
from uuid import uuid4

from infrastructure.auth.jwt_auth_service import JwtAuthService
from domain.exceptions.auth import InvalidCredentials, TokenExpired


@pytest.fixture
def auth_service():
    return JwtAuthService()


class TestJwtAuthService:
    def test_hash_and_verify_password(self, auth_service):
        hashed = auth_service.hash_password("my_secure_password")
        assert hashed != "my_secure_password"
        assert auth_service.verify_password("my_secure_password", hashed)
        assert not auth_service.verify_password("wrong_password", hashed)

    def test_create_and_decode_access_token(self, auth_service):
        user_id = uuid4()
        token = auth_service.create_access_token(user_id, "admin")
        payload = auth_service.decode_token(token)

        assert payload["sub"] == str(user_id)
        assert payload["role"] == "admin"
        assert payload["type"] == "access"

    def test_create_and_decode_refresh_token(self, auth_service):
        user_id = uuid4()
        token = auth_service.create_refresh_token(user_id)
        payload = auth_service.decode_token(token)

        assert payload["sub"] == str(user_id)
        assert payload["type"] == "refresh"

    def test_decode_invalid_token(self, auth_service):
        with pytest.raises(InvalidCredentials):
            auth_service.decode_token("invalid.token.here")

    def test_decode_token_missing_sub(self, auth_service):
        # Create a token manually without sub
        from jose import jwt
        from infrastructure.config.settings import settings

        token = jwt.encode(
            {"type": "access"},
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm,
        )
        with pytest.raises(InvalidCredentials):
            auth_service.decode_token(token)
