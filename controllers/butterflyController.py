from sqlalchemy.orm import Session
from models.butterflyModel import Butterfly
from database import database_connection
from fastapi import Depends
from schemas.buterflySchema import ButterflyCreate, ButterflyUpdate

# Todas estas funciones realizan consultas (query) en la base de datos
# Voy a especificar en comentarios lo que hace cada una.

# Función que consulta en db todas las mariposas: query READ
# db.query(Butterfly) le dice a la bd sobre que tabla tiene que hacer la consulta (Butterfly el modelo)
# .all() le dice a la bd que traiga todos los registros de la tabla
def get_butterflies(db: Session = Depends(database_connection.get_db)): 
    return db.query(Butterfly).all()

# Función que consulta en db una mariposa por su ID con método filter: query READ
def get_butterfly_by_id(db: Session, butterfly_id: int):
    butterfly = db.query(Butterfly).filter(Butterfly.id == butterfly_id).first()
    return butterfly

#  Función para crear una mariposa: query CREATE

# Fijate que los Argumentos han cambiado ahora utilizamos el tipo ButterflyCreate, ya que cuando hacemos un post no ponemos el id, para comprenderlo más mira el archivo schemas/butterflySchema.py
# El método model_dump() convierte el objeto Pydantic en un diccionario, Objeto de Js
# El método ** convierte el diccionario en argumentos clave-valor
# El método add() agrega un objeto a la sesión actual
# El método commit() guarda los cambios en la base de datos
# El método refresh() actualiza el objeto con los cambios realizados en la base de datos

def create_butterfly(db: Session, butterfly: ButterflyCreate):
    new_butterfly = Butterfly(**butterfly.model_dump())
    db.add(new_butterfly)
    db.commit()
    db.refresh(new_butterfly)
    return new_butterfly


# Función para actualizar en bd una mariposa con el método update: query UPDATE
# db.query(Butterfly) le que haga la consulta sobre la tabla representada por el modelo Butterfly (es decir, la tabla butterflies, mira tu archivo models/butterflyModel.py)
# butterfly en mínuscula es la que le llega por la petición, la nueva del usuario ('por postman')

def update_butterfly(db: Session, butterfly_id: int, butterfly: ButterflyUpdate):
    db.query(Butterfly).filter(Butterfly.id == butterfly_id).update(butterfly.model_dump())
    db.commit()
    update_butterfly = db.query(Butterfly).filter(Butterfly.id == butterfly_id).first()
    return update_butterfly

