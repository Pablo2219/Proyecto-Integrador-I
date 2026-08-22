from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field


class UsuarioUpdate(BaseModel):
    correoElectronico: Optional[EmailStr] = None
    rol: Optional[Literal["ADMINISTRADOR", "CLIENTE"]] = None
    idCliente: Optional[int] = Field(None, gt=0)
    estado: Optional[Literal["ACTIVO", "INACTIVO", "BLOQUEADO"]] = None
