from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, String, func
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Notificacion(Base):
    __tablename__ = "Notificacion"

    idNotificacion: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), primary_key=True, autoincrement=True
    )
    idCliente: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("Cliente.idCliente", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    idReserva: Mapped[Optional[int]] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("Reserva.idReserva", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )
    idPago: Mapped[Optional[int]] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("Pago.idPago", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )
    idDeuda: Mapped[Optional[int]] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey("Deuda.idDeuda", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )
    tipoNotificacion: Mapped[str] = mapped_column(
        SqlEnum("RESERVA", "QR", "PAGO", "DEUDA", "SISTEMA"), nullable=False
    )
    canal: Mapped[str] = mapped_column(
        SqlEnum("EMAIL", "SMS", "WHATSAPP", "PUSH"), nullable=False
    )
    titulo: Mapped[str] = mapped_column(String(100), nullable=False)
    mensaje: Mapped[str] = mapped_column(String(500), nullable=False)
    destinatario: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    estado: Mapped[str] = mapped_column(
        SqlEnum("PENDIENTE", "ENVIADA", "FALLIDA", "LEIDA", "ANULADA"),
        nullable=False,
        default="PENDIENTE",
    )
    fechaEnvio: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fechaLectura: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    observaciones: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    fechaCreacion: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )
    fechaActualizacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
