from fastapi import APIRouter, HTTPException, Depends
from schemas.juegos_schemas import JuegoSchema, JuegoUpdateSchema, IdCorrecto, BoolActivo
from sqlalchemy.orm import Session
from database import get_db
from models.juego import Juego
from schemas.juegos_schemas import JuegoSchema, JuegoUpdateSchema


juegos_routers = APIRouter()

NOT_FOUND = {
    404: {
        "description": "Response not found si no se encuentra el ID",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Juego no encontrado",
                }
            }
        },
    },
}

#--------------GET TODOS-------------------------------------------------------------------
@juegos_routers.get("/", response_model=list[JuegoSchema])
async def get_juegos(
    db: Session = Depends(get_db)):
    juegos = db.query(Juego).filter(Juego.activo == True).all()
    return juegos

#--------------GET BORRADOS LÓGICOS--------------------------------------------------------
@juegos_routers.get("/hidden", response_model=list[JuegoSchema])
async def get_juegos_ocultos(
    db: Session = Depends(get_db)):
    ocultos = db.query(Juego).filter(Juego.activo == False).all()
    return ocultos

#-------------- GET GENEROS----------------------------------------------------------------
@juegos_routers.get("/generos", response_model=list[str])
async def get_genero(
    db: Session = Depends(get_db)):
    generos = (
        db.query(Juego.genero).filter(Juego.activo == True)
        .distinct().order_by(Juego.genero).all()
    )
    return [g[0] for g in generos]

#distinct() evita duplicados
#el return "raro" es porque SQLalchemy genera una tupla tipo [("Accion",),("RPG",)], entonces con esa
#lista por comprension solo tomamos el primer elemento de cada tupla y devuelve ["Accion", "RPG"]
#---------------GET BY ID------------------------------------------------------------------
@juegos_routers.get(
    "/{id}",
    responses=NOT_FOUND,
    response_model=JuegoSchema,
)
async def get_juego_by_id(
    id: IdCorrecto, db: Session = Depends(get_db)):
    juego_obtenido = db.get(Juego, id)
    if juego_obtenido is not None:
        return juego_obtenido
    raise HTTPException(status_code=404, detail= "Juego no encontrada")

#ERROR RARO... get by generos solo funciona si va antes del get by ID; si van al reves
#FastAPI se queda esperando "/{id}" en lugar de "/generos" y pide un integer
#----------------------POST------------------------------------------------------------------
@juegos_routers.post("/", response_model=JuegoSchema)
async def crear_juego(
    juego_nuevo: JuegoSchema,
    db: Session = Depends(get_db)):

    juego_db = Juego(
        nombre=juego_nuevo.nombre,
        genero=juego_nuevo.genero,
        precio=juego_nuevo.precio,
        activo=juego_nuevo.activo,
    )

    db.add(juego_db)
    db.commit()
    db.refresh(juego_db)
    return juego_db

#-----------------------DELETE--------------------------------------------------------------
@juegos_routers.delete(
    "/{id}", responses=NOT_FOUND, response_model=list[JuegoSchema],
)
async def borrar_juego(
    id: IdCorrecto,
    borrado_logico: BoolActivo = True,
    db: Session = Depends(get_db)
):
    juego_obtenido = db.get(Juego, id)
    if juego_obtenido is not None:
        if borrado_logico:
            juego_obtenido.activo = False
            db.commit()
            db.refresh(juego_obtenido)
        else:
            db.delete(juego_obtenido)
            db.commit()
        return db.query(Juego).all()
    raise HTTPException(status_code=404, detail="Juego no encontrado")

#------------------PUT---------------------------------------------------------
@juegos_routers.put(
    "/{id}", responses=NOT_FOUND, response_model=JuegoSchema
)
async def editar_juego(
    id: IdCorrecto,
    juego_editar: JuegoUpdateSchema,
    db: Session = Depends(get_db),
):
    juego_obtenido = db.get(Juego, id)
    if juego_obtenido is not None:
            juego_obtenido.nombre = juego_editar.nombre
            juego_obtenido.genero = juego_editar.genero
            juego_obtenido.precio = juego_editar.precio
            juego_obtenido.activo = juego_editar.activo
            db.commit()
            db.refresh(juego_obtenido)
            return juego_obtenido
    raise HTTPException(status_code=404, detail="Juego no encontrado")