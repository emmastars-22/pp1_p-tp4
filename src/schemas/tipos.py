from typing import Annotated
from pydantic import Field

IdCorrecto = Annotated[int, Field(gt=0, desciption="ID del juego")]
StrCorto = Annotated[str, Field(min_length=2, max_length=50)]
Precio = Annotated[float, Field(gt=0, le=99999)]
BoolActivo = Annotated[bool, Field(description="¿Sigue disponible?")]