from domain.exceptions.base import DomainException


class InvalidOrder(DomainException):
    pass


class OrderNotModifiable(DomainException):
    def __init__(self) -> None:
        super().__init__("El pedido no puede ser modificado en su estado actual")
