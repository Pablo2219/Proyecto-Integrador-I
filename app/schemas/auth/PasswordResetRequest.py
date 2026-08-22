from pydantic import BaseModel, Field


class PasswordResetRequest(BaseModel):
    token: str = Field(..., min_length=20)
    nuevaContrasena: str = Field(..., min_length=8, max_length=72)
