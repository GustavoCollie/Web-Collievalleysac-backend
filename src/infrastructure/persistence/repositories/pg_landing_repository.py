from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.landing_section import LandingSection
from domain.ports.repositories.landing_repository import LandingRepository
from infrastructure.persistence.models.landing_model import LandingSectionORM


class PgLandingRepository(LandingRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    def _to_domain(self, orm: LandingSectionORM) -> LandingSection:
        return LandingSection(
            id=orm.id,
            section_key=orm.section_key,
            title=orm.title,
            subtitle=orm.subtitle,
            content=orm.content or {},
            display_order=orm.display_order,
            is_visible=orm.is_visible,
            updated_by=orm.updated_by,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    async def find_all_visible(self) -> list[LandingSection]:
        stmt = (
            select(LandingSectionORM)
            .where(LandingSectionORM.is_visible == True)
            .order_by(LandingSectionORM.display_order)
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(orm) for orm in result.scalars().all()]

    async def find_all(self) -> list[LandingSection]:
        stmt = select(LandingSectionORM).order_by(LandingSectionORM.display_order)
        result = await self._session.execute(stmt)
        return [self._to_domain(orm) for orm in result.scalars().all()]

    async def find_by_key(self, section_key: str) -> LandingSection | None:
        stmt = select(LandingSectionORM).where(LandingSectionORM.section_key == section_key)
        result = await self._session.execute(stmt)
        orm = result.scalar_one_or_none()
        return self._to_domain(orm) if orm else None

    async def save(self, section: LandingSection) -> LandingSection:
        orm = LandingSectionORM(
            id=section.id,
            section_key=section.section_key,
            title=section.title,
            subtitle=section.subtitle,
            content=section.content,
            display_order=section.display_order,
            is_visible=section.is_visible,
            updated_by=section.updated_by,
        )
        self._session.add(orm)
        await self._session.commit()
        await self._session.refresh(orm)
        return self._to_domain(orm)

    async def update(self, section: LandingSection) -> LandingSection:
        orm = await self._session.get(LandingSectionORM, section.id)
        if orm:
            orm.title = section.title
            orm.subtitle = section.subtitle
            orm.content = section.content
            orm.display_order = section.display_order
            orm.is_visible = section.is_visible
            orm.updated_by = section.updated_by
            await self._session.commit()
            await self._session.refresh(orm)
            return self._to_domain(orm)
        return section

    async def delete(self, section_id: UUID) -> None:
        orm = await self._session.get(LandingSectionORM, section_id)
        if orm:
            await self._session.delete(orm)
            await self._session.commit()
