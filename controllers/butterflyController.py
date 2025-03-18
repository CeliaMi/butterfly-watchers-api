from sqlalchemy.orm import Session
from models import butterflyModel 
from database import database_connection
from fastapi import Depends



# Función para obtener todas las mariposas
def get_butterflies(db: Session = Depends(database_connection.get_db)): 
    return db.query(butterflyModel.Butterfly).all()

