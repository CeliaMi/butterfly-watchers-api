from sqlalchemy import create_engine
from config import settings
# iportamos cosas de sqlachemy para poder generar una sesión
# y poder crear la Base sobre la que heredaran los Modelos
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

#Esto es un extra para el tipado (es prescindible)
from typing import Generator


# Crear el motor de conexión de SQLAlchemy para PostgreSQL
engine = create_engine(settings.DATABASE_URL, echo=True)

with engine.connect() as connection:
    print("Conexión exitosa a PostgreSQL")

# Crear una sesión local de SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Función que obtiene la sesión de base de datos


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base para los modelos de SQLAlchemy
Base = declarative_base()

# Crear las tablas en la base de datos si no existen basandose en los modelos
Base.metadata.create_all(bind=engine)