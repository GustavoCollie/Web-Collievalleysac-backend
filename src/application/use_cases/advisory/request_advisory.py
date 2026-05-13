from datetime import date

from domain.entities.advisory import AdvisoryRequest, Urgency
from domain.ports.repositories.advisory_repository import AdvisoryRepository
from application.dtos.advisory_dto import CreateAdvisoryInput


class RequestAdvisoryUseCase:
    def __init__(self, advisory_repo: AdvisoryRepository):
        self._advisory_repo = advisory_repo

    async def execute(self, input: CreateAdvisoryInput) -> AdvisoryRequest:
        preferred = None
        if input.preferred_date:
            preferred = date.fromisoformat(input.preferred_date)

        request = AdvisoryRequest(
            user_id=input.user_id,
            crop_type=input.crop_type,
            problem_description=input.problem_description,
            preferred_date=preferred,
            urgency=Urgency(input.urgency),
        )
        return await self._advisory_repo.save(request)
