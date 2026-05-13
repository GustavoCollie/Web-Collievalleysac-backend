from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.advisory import AdvisoryRequest, AdvisoryStatus, Urgency
from domain.ports.repositories.advisory_repository import AdvisoryRepository
from infrastructure.persistence.models.advisory_model import AdvisoryRequestORM


class PgAdvisoryRepository(AdvisoryRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    def _to_domain(self, orm: AdvisoryRequestORM) -> AdvisoryRequest:
        return AdvisoryRequest(
            id=orm.id,
            user_id=orm.user_id,
            crop_type=orm.crop_type,
            problem_description=orm.problem_description,
            preferred_date=orm.preferred_date,
            urgency=Urgency(orm.urgency),
            status=AdvisoryStatus(orm.status),
            advisor_notes=orm.advisor_notes or "",
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    async def save(self, request: AdvisoryRequest) -> AdvisoryRequest:
        orm = AdvisoryRequestORM(
            id=request.id,
            user_id=request.user_id,
            crop_type=request.crop_type,
            problem_description=request.problem_description,
            preferred_date=request.preferred_date,
            urgency=request.urgency.value,
            status=request.status.value,
            advisor_notes=request.advisor_notes,
        )
        self._session.add(orm)
        await self._session.commit()
        await self._session.refresh(orm)
        return self._to_domain(orm)

    async def find_by_id(self, request_id: UUID) -> AdvisoryRequest | None:
        orm = await self._session.get(AdvisoryRequestORM, request_id)
        return self._to_domain(orm) if orm else None

    async def find_by_user(self, user_id: UUID) -> list[AdvisoryRequest]:
        stmt = (
            select(AdvisoryRequestORM)
            .where(AdvisoryRequestORM.user_id == user_id)
            .order_by(AdvisoryRequestORM.created_at.desc())
        )
        result = await self._session.execute(stmt)
        return [self._to_domain(orm) for orm in result.scalars().all()]

    async def update(self, request: AdvisoryRequest) -> AdvisoryRequest:
        orm = await self._session.get(AdvisoryRequestORM, request.id)
        if orm:
            orm.status = request.status.value
            orm.advisor_notes = request.advisor_notes
            orm.preferred_date = request.preferred_date
            await self._session.commit()
            await self._session.refresh(orm)
            return self._to_domain(orm)
        return request
