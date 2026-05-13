from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.user import Role, User
from domain.ports.repositories.user_repository import UserRepository
from infrastructure.persistence.models.user_model import UserORM


class PgUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    def _to_domain(self, orm: UserORM) -> User:
        return User(
            id=orm.id,
            email=orm.email,
            hashed_password=orm.hashed_password,
            full_name=orm.full_name,
            phone=orm.phone or "",
            role=Role(orm.role),
            is_active=orm.is_active,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    def _to_orm(self, user: User) -> UserORM:
        return UserORM(
            id=user.id,
            email=user.email,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            phone=user.phone,
            role=user.role.value,
            is_active=user.is_active,
        )

    async def save(self, user: User) -> User:
        orm = self._to_orm(user)
        self._session.add(orm)
        await self._session.commit()
        await self._session.refresh(orm)
        return self._to_domain(orm)

    async def find_by_id(self, user_id: UUID) -> User | None:
        result = await self._session.get(UserORM, user_id)
        return self._to_domain(result) if result else None

    async def find_by_email(self, email: str) -> User | None:
        stmt = select(UserORM).where(UserORM.email == email.lower())
        result = await self._session.execute(stmt)
        orm = result.scalar_one_or_none()
        return self._to_domain(orm) if orm else None

    async def find_all(self) -> list[User]:
        stmt = select(UserORM).order_by(UserORM.created_at.desc())
        result = await self._session.execute(stmt)
        return [self._to_domain(orm) for orm in result.scalars().all()]

    async def update(self, user: User) -> User:
        orm = await self._session.get(UserORM, user.id)
        if orm:
            orm.email = user.email
            orm.full_name = user.full_name
            orm.phone = user.phone
            orm.role = user.role.value
            orm.is_active = user.is_active
            await self._session.commit()
            await self._session.refresh(orm)
            return self._to_domain(orm)
        return user

    async def delete(self, user_id: UUID) -> None:
        orm = await self._session.get(UserORM, user_id)
        if orm:
            await self._session.delete(orm)
            await self._session.commit()
