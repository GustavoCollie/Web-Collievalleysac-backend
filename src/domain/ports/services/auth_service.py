from abc import ABC, abstractmethod
from uuid import UUID


class AuthService(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str: ...

    @abstractmethod
    def verify_password(self, plain: str, hashed: str) -> bool: ...

    @abstractmethod
    def create_access_token(self, user_id: UUID, role: str) -> str: ...

    @abstractmethod
    def create_refresh_token(self, user_id: UUID) -> str: ...

    @abstractmethod
    def decode_token(self, token: str) -> dict: ...
