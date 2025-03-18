from sqlalchemy.orm import Session
from models.butterflyModel import Butterfly
from database import database_connection
from fastapi import Depends
from schemas.buterflySchema import ButterflyCreate

# Todas estas funciones realizan consultas (query) en la base de datos
# Voy a especificar en un comentario lo que consulta cada una de ellas

# Función que consulta READ todas las mariposas
def get_butterflies(db: Session = Depends(database_connection.get_db)): 
    return db.query(Butterfly).all()

# Función que consulta READ una mariposa por su ID método filter
def get_butterfly_by_id(db: Session, butterfly_id: int):
    butterfly = db.query(Butterfly).filter(Butterfly.id == butterfly_id).first()
    return butterfly

# # Función que CREA una mariposa método add
# # El método add() agrega un objeto a la sesión actual
# # El método commit() guarda los cambios en la base de datos
# # El método refresh() actualiza el objeto con los cambios realizados en la base de datos
def create_butterfly(db: Session, butterfly: ButterflyCreate):
    new_butterfly = Butterfly(**butterfly.dict())
    db.add(new_butterfly)
    db.commit()
    db.refresh(new_butterfly)
    return new_butterfly


# # Función que ACTUALIZA una mariposa método update
# def update_butterfly(db: Session, butterfly_id: int, butterfly: Butterfly):
#     db.query(Butterfly).filter(Butterfly.id == butterfly_id).update(butterfly.dict())
#     db.commit()
#     return butterfly

