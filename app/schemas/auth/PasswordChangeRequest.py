from pydantic import BaseModel, Field


class PasswordChangeRequest(BaseModel):
    contrasenaActual: str = Field(..., min_length=8, max_length=72)
    nuevaContrasena: str = Field(..., min_length=8, max_length=72)
