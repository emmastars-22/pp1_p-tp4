from pydantic import BaseModel
from .tipos import BoolActivo, Precio, StrCorto, IdCorrecto

class JuegoSchema(BaseModel):
    id: IdCorrecto
    nombre: StrCorto
    genero: StrCorto
    precio: Precio
    activo: BoolActivo = True

class JuegoUpdateSchema(BaseModel):
    nombre: StrCorto
    genero: StrCorto
    precio: Precio
    activo: BoolActivo