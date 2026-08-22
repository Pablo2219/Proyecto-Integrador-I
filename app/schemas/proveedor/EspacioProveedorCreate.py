from typing import Optional
from pydantic import BaseModel, Field
class EspacioProveedorCreate(BaseModel):
    idSector: int = Field(..., gt=0)
    codigoEspacio: str = Field(..., min_length=1, max_length=20)
    tipoEspacio: str = Field("REGULAR", max_length=20)
    descripcion: Optional[str] = Field(None, max_length=250)
    latitud: float = Field(..., ge=-90, le=90)
    longitud: float = Field(..., ge=-180, le=180)
