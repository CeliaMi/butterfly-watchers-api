from fastapi import FastAPI
from database.database_connection import engine
from routes.butterflyRouter import router

app = FastAPI()

app.include_router(router)

with engine.connect() as connection:
    print("Conexión exitosa a PostgreSQL")