from typing import Optional
from pydantic import BaseModel, Field
class SectorCreate(BaseModel):
    nombreSector: str = Field(..., min_length=2, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=250)
    latitud: float = Field(..., ge=-90, le=90)
    longitud: float = Field(..., ge=-180, le=180)
    precioHora: float = Field(0, ge=0)
