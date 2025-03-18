from fastapi import APIRouter
from controllers import butterflyController
from schemas.buterflySchema import Butterfly
from schemas.buterflySchema import ButterflyCreate
from database.database_connection import get_db
from sqlalchemy.orm import Session
from fastapi import Depends


router = APIRouter()

# Ruta "/butterflies/" GET para obtener todas las mariposas
@router.get("/butterflies/")
def read_butterflies(db: Session = Depends(get_db)):
        return butterflyController.get_butterflies(db)

# Ruta "/butterflies/{butterfly_id}" GET para obtener una mariposa por su ID
# Se define la ruta en la primera línea y la respuestas que dará la ruta.
# En la segunda línea se define una función que recibe el parámetro butterfly_id y la Session de la base de datos, inyectada por el decorador Depends
# en la tercera línea se llama al controlador que queremos asociar a esta ruta
@router.get("/butterflies/{butterfly_id}", response_model=Butterfly)
def read_one_butterfly(butterfly_id: int, db: Session = Depends(get_db)):
    return butterflyController.get_butterfly_by_id(db, butterfly_id)


# # Ruta "/butterflies/" POST para crear una mariposa
@router.post("/butterflies", response_model=Butterfly)
def create_butterfly(butterfly: ButterflyCreate, db: Session = Depends(get_db)):
    return butterflyController.create_butterfly(db, butterfly)

# # Ruta "/butterflies/{butterfly_id}" PUT para actualizar una mariposa por su ID
# @router.put("/butterflies/{butterfly_id}", response_model=Butterfly)
# def update_butterfly(butterfly_id: int, butterfly: Butterfly, db: Session = Depends(get_db)):
#     return butterflyController.update_butterfly(db, butterfly_id, butterfly)

