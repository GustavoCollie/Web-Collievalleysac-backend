from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.persistence.database import get_session
from infrastructure.persistence.repositories.pg_user_repository import PgUserRepository
from infrastructure.persistence.repositories.pg_landing_repository import PgLandingRepository
from infrastructure.auth.jwt_auth_service import JwtAuthService
from domain.ports.repositories.user_repository import UserRepository
from domain.ports.repositories.landing_repository import LandingRepository
from domain.ports.services.auth_service import AuthService


def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> UserRepository:
    return PgUserRepository(session)


def get_landing_repository(
    session: AsyncSession = Depends(get_session),
) -> LandingRepository:
    return PgLandingRepository(session)


def get_auth_service() -> AuthService:
    return JwtAuthService()
