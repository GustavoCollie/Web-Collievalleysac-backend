from pydantic import BaseModel, EmailStr, Field
from domain.entities.user import Role


class UpdateUserRequest(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    role: Role | None = None
    is_active: bool | None = None


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=150)
    phone: str = ""
    role: Role = Role.IMPORTADOR


class MetricsResponse(BaseModel):
    total_users: int
    active_users: int
    total_orders: int
    total_brokerage_requests: int
    total_advisory_requests: int
    users_by_role: dict[str, int]
