from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field


class UsuarioCreate(BaseModel):
    nombreUsuario: str = Field(..., min_length=4, max_length=50)
    correoElectronico: EmailStr
    contrasena: str = Field(..., min_length=8, max_length=72)
    rol: Literal["ADMINISTRADOR", "CLIENTE"]
    idCliente: Optional[int] = Field(None, gt=0)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombreUsuario": "cliente02",
                    "correoElectronico": "cliente02@parksmart.com",
                    "contrasena": "Cliente123*",
                    "rol": "CLIENTE",
                    "idCliente": 1,
                },
                {
                    "nombreUsuario": "admin02",
                    "correoElectronico": "admin02@parksmart.com",
                    "contrasena": "Admin123*",
                    "rol": "ADMINISTRADOR",
                    "idCliente": None,
                },
            ]
        }
    }
