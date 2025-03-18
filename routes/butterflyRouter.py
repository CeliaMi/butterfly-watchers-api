from fastapi import APIRouter
from controllers import butterflyController
from schemas.buterflySchema import Butterfly 


router = APIRouter()

# Ruta "/butterflies/" GET para obtener todas las mariposas
router.get("/butterflies/", response_model=list[Butterfly])(butterflyController.get_butterflies)

