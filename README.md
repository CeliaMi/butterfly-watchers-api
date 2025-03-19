# fast-api CRUD Básico

Autoria: Celia Millán
Etiquetas: Python, crud, fastApi
Fecha de publicación: 10 de marzo de 2025
documentación oficial: https://fastapi.tiangolo.com/

Vamos a crear una aplicación para guardar avistamientos de mariposas.🦋👀

¿Porqué de Mariposas?

Te recomiendo [leer este artículo](https://www.nationalgeographic.com.es/mundo-animal/por-que-estan-desapareciendo-mariposas_24406) de la revista National Geographic👇

<aside>

> [**¿Por qué están desapareciendo las mariposas?**](https://www.nationalgeographic.com.es/mundo-animal/por-que-estan-desapareciendo-mariposas_24406) Un declive alarmante que amenaza los ecosistemas, tanto de Europa como de Estados Unidos
> 
</aside>

Después de reflexionar un poco sobre las mariposas y su futuro volvamos a nuestra app para poder guardar datos y llevar un registro de las que aún quedan.

Esta app es sin imágenes, más en adelante sobre este mismo proyecto añadiremos la gestión de imágenes.

A nivel técnico esta práctica está pensada para aprender a codear un CRUD sencillo con Python y `fastApi` con un fuerte enfoque hacía `Node` y `Express` de JavaScript.

¡Comenzamos!

| Lenguaje | **Python** |
| --- | --- |
| Framework | **fast-API** |
| Objetivo | **CRUD básico** |
| Enfoque | para desarrolladoras de **JavaScript** |
| Temática | Api para guardar **avistamientos de Mariposas** |

*Cosas que damos por hechas: tener postgres, python y un editor de código instalados en tu máquina*
<details>
<summary>
1️⃣ Creamos la base de datos:
</summary>

En este ejemplo la base de datos que vamos a utilizar es de **postgres**, pero podría ser con otras ( de ser así ya sabes, pregunta a Geppetto)

![image.png](./files/image.png)

</details>

<details>
<summary> 2️⃣ Estructura de carpetas siguiendo el estilo de Node.js y Express.js</summary>
    
![image.png](./files/image%201.png)
![image.png](./files/image%202.png)
</details>

<details>
<summary>
3️⃣ Entorno de desarrollo
</summary>

1️⃣ Necesitamos crear **un entorno** para guardar todos los paquetes necesarios de Python.

Lo harás creando una carpeta venv, si no todo se te instalara de manera global en tu ordenador.

`venv` es el módulo estándar de Python que permite **crear entornos virtuales**

Se crea todito todo con este comando👇

```bash
python -m venv venv
```

<aside>
👮‍♀️

Si estas haciendo control de versión recuerda crear un `.gitignore` y nombrar `venv/`

</aside>

Para poder activar este entorno escribe el siguiente comando en tu terminal de `Bash`

```bash
source venv/Scripts/activate
```

Si no tienes Bash el comando sería este en tu consola PoweShell👇

```powershell
venv\Scripts\Activate.ps1
```

Sabrás que está activado porqué en tu terminal verás:

![image.png](./files/image%203.png)

Bien, ahora vamos a instalamos todo lo necesario

```python
pip install fastApi uvicorn pydantic sqlalchemy psycopg2-binary SQLAlchemy-Utils dotenv 
```

- **`FastAPI`**: Framework web moderno y rápido para construir APIs con Python y type hints.
- **`Uvicorn`**: Servidor ASGI ligero y eficiente para ejecutar aplicaciones FastAPI y Django.
- **`Pydantic`**: Biblioteca para validación de datos basada en anotaciones de tipo de Python.
- **`SQLAlchemy`**: ORM y toolkit SQL para interactuar con bases de datos en Python.
- **`psycopg2-binary`**: Conector de PostgreSQL para Python que permite ejecutar consultas SQL.
- **`dotenv`**: Carga variables de entorno desde un archivo `.env` en Python.

👮‍♀️🚨**Atención**🚨👮‍♀️

Recuerda no olvides el archivo `.gitignore`.

![image.png](./files/image%204.png)
</details>
<details>
<summary>
4️⃣Creamos nuestra APP y nos Conectamos a la Base de datos
</summary>
Creamos nuestra app básica en el archivo `app.py`

```python
from fastapi import FastAPI

app = FastAPI()

with engine.connect() as connection:
# esta línea es la que veremos después en  nuestra consola para comprobar la conexión
    print("Conexión exitosa a PostgreSQL")
```

### Conexión a Base de datos

Ahora vamos a crear la conexión a nuestra base de datos en el archivo `database_connection.py`

```python
from sqlalchemy import create_engine

# Crear el motor de conexión de SQLAlchemy para PostgreSQL
engine = create_engine("postgresql://username:password@localhost/dbname", echo=True)
```

Para no exponer nuestros datos utilizamos variables de entorno ( lo instalamos antes con dotenv)

archivo `.env`

```markdown
DATABASE_URL= postgresql://username:password@localhost/dbname
```

archivo `config.py`

```python
import os

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Settings()
```

archivo `database_connection.py`

```python
from sqlalchemy import create_engine
👉from config import settings

# Aquí cambiamos el enlace por nuestra constante
# así nuestros datos quedan protegidos en el .env
engine = create_engine(👉settings.DATABASE_URL, echo=True)
```

Ahora vamos a comprobar si en consola aparece el mensaje para ver que la conexión ha sido exitosa👇

![image.png](./files/image%205.png)

Vale, ahora que ya tenemos nuestra conexión exitosa, vamos hacer unos ajustes en `database_connection.py` marco todo lo nuevo con 👉

estamos haciendo dos cosas , crear la sesión de la base de datos y crear la clase Base sobre la que heredaran todos los Modelos.

```python
from sqlalchemy import create_engine
from config import settings
# iportamos cosas de sqlachemy para poder generar una sesión
# y poder crear la Base sobre la que heredaran los Modelos
👉from sqlalchemy.orm import sessionmaker
👉from sqlalchemy.ext.declarative import declarative_base

#Esto es un extra para el tipado (es prescindible)
👉from typing import Generator

engine = create_engine(settings.DATABASE_URL, echo=True)

# Crear una sesión local de SQLAlchemy
👉 SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Función que obtiene la sesión de base de datos
👉 def get_db() -> Generator[SessionLocal, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
 
# Base para los modelos de SQLAlchemy
👉 Base = declarative_base()

# Crear las tablas en la base de datos si no existen basandose en los modelos
👉 Base.metadata.create_all(bind=engine)
```
</details>
<details>
<summary>
 5️⃣Creamos nuestro modelo y controladores
</summary>
    
Comencemos a definir nuestros **modelos** `butterflyModel.py`

```python
# Base es una clase base que definimos en nuestro archivo database_connection 
# todos los modelos deben heredar en SQLAlchemy
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
```

Una vez que ya tenemos nuestro modelo en vamos a definir nuestro **controlador**, es decir, la función que activa la lógica de la consulta a la base de datos y la devuelve en JSON

`butterflyController.py`

```python
from sqlalchemy.orm import Session
from models import butterflyModel 

# Función para obtener todas las mariposas
def get_butterflies(db: Session):
    return db.query(butterflyModel.Butterfly).all()
```

Este es un controlador básico para hacer una query de READ sobre la base de datos a través del método `.all()`, estamos preparando nuestra ruta GET.
<details>
<summary>Bien, estamos viendo cosas nuevas ¿ Qué es eso de Session que pasamos por parámetro?
</summary>



 **Cada petición HTTP necesita su propia sesión de base de datos** para evitar problemas de concurrencia. **La sesión se pasa como parámetro** a los controladores para evitar múltiples conexiones innecesarias. **`query.all()` necesita una sesión activa,** SQLAlchemy no sabe **qué conexión usar** para ejecutar la consulta. **Por eso, la `Session` es obligatoria** en cada función que interactúa con la base de datos.


<aside> 

🗣
**en SQLAlchemy `Session` es como un "túnel" hacia la base de datos. Si no lo pasamos, no podemos hacer consultas.** 

</aside>

Cuando decimos que cada petición necesita su propia sesión, **no significa que estemos creando una nueva conexión de base de datos en cada función**.
    
**Lo que significa es que cada petición debe tener una sesión aislada para evitar interferencias entre peticiones concurrentes.**
    
La clave está en que FastAPI maneja el ciclo de vida de la sesión correctamente, asegurando que:
    
- **Cada petición tenga su propia instancia de sesión** (aislación de transacciones).
- **Se reutilicen conexiones de base de datos** eficientemente, sin crear una nueva conexión en cada función.
- **Se cierre adecuadamente la sesión** al final de la petición.
    
Podríamos inyectarle aquí la sesión para que las rutas queden más limpias
    
`router.py`
    
```python
@router.get("/butterflies", response_model=list[Butterfly])(butterflyController.get_butterflies())
```
    
 `controller.py`
    
```python
    from sqlalchemy.orm import Session
    from models.butterflyModel import Butterfly
    from database import database_connection
    from fastapi import Depends
    
    # Función que consulta en db todas las mariposas: query READ
    # Dependencia de ssesion inyectada aquí dentro.
    def get_butterflies(db: Session = Depends(database_connection.get_db)): 
        return db.query(Butterfly).all()
```
    
Pero esto solo funciona para este controlador, en el resto el inyectado directo de la Session no funciona, ya que hay que enviarle más dependencias y al final si tenemos que hacer una segunda función en el rutado, asique es una pena pero fastApi no nos dejaaa 😞

</details>
</details>
<details>
<summary>
6️⃣Creamos nuestras Rutas
</summary>

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import database_connection
from controllers import butterflyController
from schemas.buterflySchema import Butterfly 

router = APIRouter()

# Ruta "/butterflies" GET para obtener todas las mariposas

@router.get("/butterflies", response_model=list[Butterfly])
def get_butterflies(db: Session = Depends(database_connection.get_db)):
    return butterflyController.get_butterflies(db=db)
```

Llegó la hora de la verdad, vamos a comprobar si nuestro code funciona: escribe en tu terminal 

```bash
uvicorn app:app --reload
```

Abre alguna herramienta como `postman` para testear tu endpoints.

Si tu array está vacío es porqué tu tabla no tiene ningún registro, para poder comprobarlo mejor te recomiendo que insertes manualmente mariposas desde tu consola de `SQL shell.`

![image.png](./files/image%206.png)

En el repositorio encontrarás la explicación del resto de métodos del CRUD a través de comentarios.
No olvides que fastApi hace la documentación de forma automática en swagger simplemente tienes que consultar tu enlace local añadiendo `docs#/`:

- http://127.0.0.1:8000/docs#/

Recuerda, si vas a subir tu repo a github no olvides crear un archivo `requirements.txt`

```powershell
pip freeze > requirements.txt
```
</details>

Si lo que quieres es instalar este repositorio:

```powershell
python -m venv venv
source venv/Scripts/activate  # En Windows (o venv\Scripts\activate en CMD)
pip install -r requirements.txt
```

