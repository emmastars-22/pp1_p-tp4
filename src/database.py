from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

url = "sqlite:///./base_de_datos.db"

engine = create_engine(url, connect_args={"check_same_thread":False})
#para Fastapi hace falta el check_same_thread:False
#engine es el motor que prepara la base de datos

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#cada interacción se hace a través de una sesión
#la sesion permite conectarse a través de engine

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()