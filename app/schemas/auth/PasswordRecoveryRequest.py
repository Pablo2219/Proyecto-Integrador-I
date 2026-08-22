from typing import Literal

from pydantic import BaseModel, Field


class PasswordRecoveryRequest(BaseModel):
    usuarioOCorreo: str = Field(..., min_length=3, max_length=120)
    canal: Literal["EMAIL", "SMS", "WHATSAPP"] = "EMAIL"
