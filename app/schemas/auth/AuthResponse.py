from app.schemas.usuario.UsuarioResponse import UsuarioResponse
from pydantic import BaseModel


class AuthResponse(BaseModel):
    accessToken: str
    tokenType: str = "bearer"
    expiresIn: int
    usuario: UsuarioResponse
