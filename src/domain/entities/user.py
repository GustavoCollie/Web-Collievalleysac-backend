from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class Role(str, Enum):
    ADMIN = "admin"
    IMPORTADOR = "importador"
    EXPORTADOR_BROKER = "exportador_broker"
    AGRICULTOR = "agricultor"
    EXPORTADOR_COLLIE = "exportador_collie"


@dataclass
class User:
    email: str
    full_name: str
    role: Role
    hashed_password: str = ""
    phone: str = ""
    id: UUID = field(default_factory=uuid4)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None
