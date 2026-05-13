class DomainException(Exception):
    def __init__(self, message: str = "Error de dominio"):
        self.message = message
        super().__init__(self.message)


class EntityNotFound(DomainException):
    def __init__(self, entity: str, identifier: str = ""):
        msg = f"{entity} no encontrado"
        if identifier:
            msg = f"{entity} con id '{identifier}' no encontrado"
        super().__init__(msg)


class DuplicateEntity(DomainException):
    def __init__(self, entity: str, field: str = ""):
        msg = f"{entity} duplicado"
        if field:
            msg = f"{entity} con {field} ya existe"
        super().__init__(msg)
