from pydantic import BaseModel

# En este archivo se definen los esquemas de Pydantic para validar los datos de entrada y salida de las rutas de la API
# Se definen dos clases, ButterflyBase y Butterfly, que heredan de BaseModel

class ButterflyBase(BaseModel):
    species: str
    location: str
    specimens: int

class ButterflyCreate(ButterflyBase):
    pass

class Butterfly(ButterflyBase):
    id: int

    class Config:
        orm_mode = True