from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    usuario: str = Field(..., min_length=3, max_length=120)
    contrasena: str = Field(..., min_length=8, max_length=72)

    model_config = {
        "json_schema_extra": {
            "example": {"usuario": "admin", "contrasena": "Admin123*"}
        }
    }
