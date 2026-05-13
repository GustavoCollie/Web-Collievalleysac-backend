from dataclasses import dataclass
from datetime import date

from domain.exceptions.base import DomainException


@dataclass(frozen=True)
class DateRange:
    start: date
    end: date

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise DomainException("La fecha de inicio no puede ser posterior a la de fin")

    def contains(self, d: date) -> bool:
        return self.start <= d <= self.end
