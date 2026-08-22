from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

class RegisterRequest(BaseModel):
    nombreUsuario: str = Field(..., min_length=4, max_length=50)
    correoElectronico: EmailStr
    contrasena: str = Field(..., min_length=8, max_length=72)
    rol: Literal["CLIENTE", "PROVEEDOR"]
    identificacion: Optional[str] = Field(None, min_length=6, max_length=20)
    nombre: Optional[str] = Field(None, max_length=50)
    primerApellido: Optional[str] = Field(None, max_length=50)
    segundoApellido: Optional[str] = Field(None, max_length=50)
    telefono: str = Field(..., min_length=8, max_length=20)
    direccion: Optional[str] = Field(None, max_length=250)
    nombreComercial: Optional[str] = Field(None, max_length=120)
    identificacionFiscal: Optional[str] = Field(None, max_length=30)
    aceptaPrivacidad: bool

    @field_validator("contrasena")
    @classmethod
    def validar_contrasena(cls, value):
        if not any(c.isupper() for c in value) or not any(c.islower() for c in value) or not any(c.isdigit() for c in value):
            raise ValueError("La contraseña debe incluir mayúscula, minúscula y número.")
        return value
