from database import Base
from sqlalchemy import Boolean, Column, Integer, String, Float

class Juego(Base):
    __tablename__ = "juegos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    genero = Column(String)
    precio = Column(Float)
    activo = Column(Boolean)

#models: son clases que representan tablas en la base de datos
#se deben importar las clases de tipos de datos para construir las columnas del modelo
#se usa de referencia el schema JuegoSchema(BaseModel)