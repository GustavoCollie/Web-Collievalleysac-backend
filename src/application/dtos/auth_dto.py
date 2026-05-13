from dataclasses import dataclass
from domain.entities.user import Role


@dataclass
class RegisterInput:
    email: str
    password: str
    full_name: str
    role: Role
    phone: str = ""


@dataclass
class LoginInput:
    email: str
    password: str


@dataclass
class AuthTokensOutput:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@dataclass
class RefreshInput:
    refresh_token: str
