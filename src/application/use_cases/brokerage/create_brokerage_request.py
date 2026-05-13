from domain.entities.brokerage import BrokerageRequest
from domain.ports.repositories.brokerage_repository import BrokerageRepository
from application.dtos.brokerage_dto import CreateBrokerageInput


class CreateBrokerageRequestUseCase:
    def __init__(self, brokerage_repo: BrokerageRepository):
        self._brokerage_repo = brokerage_repo

    async def execute(self, input: CreateBrokerageInput) -> BrokerageRequest:
        request = BrokerageRequest(
            user_id=input.user_id,
            origin_country=input.origin_country,
            dest_country=input.dest_country,
            product_type=input.product_type,
            volume_kg=input.volume_kg,
            certifications=input.certifications,
            notes=input.notes,
        )
        return await self._brokerage_repo.save(request)
