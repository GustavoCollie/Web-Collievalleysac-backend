from domain.exceptions.base import DomainException


class InvalidCredentials(DomainException):
    def __init__(self) -> None:
        super().__init__("Credenciales inválidas")


class TokenExpired(DomainException):
    def __init__(self) -> None:
        super().__init__("Token expirado")


class InsufficientPermissions(DomainException):
    def __init__(self) -> None:
        super().__init__("Permisos insuficientes para esta acción")
