# Base es una clase base que definimos en nuestro archivo database_connection 
# Todos los modelos deben heredar en SQLAlchemy
# Base le dice a SQLAlchemy que esta clase representa una tabla en la base de datos
from database.database_connection import Base

# Aquí importamos clases y funciones de SQLAlchemy para definir
# las columnas de la tabla en la base de datos
from sqlalchemy import Column, Integer, String

class Butterfly(Base):
    __tablename__ = 'butterflies'

    id = Column(Integer, primary_key=True, index=True)
    species = Column(String)
    location = Column(String)
    specimens = Column(Integer)