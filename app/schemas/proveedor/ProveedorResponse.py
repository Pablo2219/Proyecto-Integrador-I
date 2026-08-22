from datetime import datetime
from typing import Optional
from pydantic import BaseModel
class ProveedorResponse(BaseModel):
    idProveedor: int
    nombreComercial: str
    identificacionFiscal: Optional[str] = None
    telefono: str
    correoElectronico: str
    direccion: Optional[str] = None
    estado: str
    fechaCreacion: datetime
    fechaActualizacion: datetime
