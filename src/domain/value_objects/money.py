from dataclasses import dataclass

from domain.exceptions.base import DomainException


@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise DomainException("El monto no puede ser negativo")
        if len(self.currency) != 3:
            raise DomainException("Código de moneda debe tener 3 caracteres")
