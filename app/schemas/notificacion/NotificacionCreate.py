from typing import Literal, Optional

from pydantic import BaseModel, Field


class NotificacionCreate(BaseModel):
    idCliente: int = Field(..., gt=0)
    idReserva: Optional[int] = Field(None, gt=0)
    idPago: Optional[int] = Field(None, gt=0)
    idDeuda: Optional[int] = Field(None, gt=0)
    tipoNotificacion: Literal["RESERVA", "QR", "PAGO", "DEUDA", "SISTEMA"]
    canal: Literal["EMAIL", "SMS", "WHATSAPP", "PUSH"]
    titulo: str = Field(..., min_length=3, max_length=100)
    mensaje: str = Field(..., min_length=5, max_length=500)
    destinatario: Optional[str] = Field(None, max_length=150)
    observaciones: Optional[str] = Field(None, max_length=250)
    enviarAhora: bool = True

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "idCliente": 1,
                    "tipoNotificacion": "SISTEMA",
                    "canal": "SMS",
                    "titulo": "Reserva próxima",
                    "mensaje": "Tu reserva inicia dentro de 30 minutos.",
                    "destinatario": "+50688889999",
                    "enviarAhora": True,
                },
                {
                    "idCliente": 1,
                    "tipoNotificacion": "PAGO",
                    "canal": "WHATSAPP",
                    "titulo": "Pago confirmado",
                    "mensaje": "El pago fue registrado correctamente.",
                    "destinatario": "+50688889999",
                    "enviarAhora": True,
                },
            ]
        }
    }
