from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UsuarioResponse(BaseModel):
    idUsuario: int
    idRol: int
    idCliente: Optional[int]
    nombreUsuario: str
    correoElectronico: str
    rol: str
    estado: str
    ultimoAcceso: Optional[datetime]
    fechaCreacion: datetime
    fechaActualizacion: datetime
