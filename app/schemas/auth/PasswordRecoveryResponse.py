from typing import Optional

from pydantic import BaseModel


class PasswordRecoveryResponse(BaseModel):
    mensaje: str
    canal: str
    tokenRestablecimiento: Optional[str] = None
