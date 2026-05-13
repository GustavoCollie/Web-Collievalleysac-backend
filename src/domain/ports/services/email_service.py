from abc import ABC, abstractmethod


class EmailService(ABC):
    @abstractmethod
    async def send_welcome(self, to_email: str, full_name: str) -> None: ...

    @abstractmethod
    async def send_order_confirmation(self, to_email: str, order_id: str) -> None: ...

    @abstractmethod
    async def send_advisory_scheduled(self, to_email: str, date: str) -> None: ...
