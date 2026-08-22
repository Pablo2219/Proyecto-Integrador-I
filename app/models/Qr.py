"""
---------------------------------------------------------
Proyecto: ParkSmart - Sistema de Parqueo Inteligente
Archivo: Qr.py

Descripcion:
Modelo ORM que representa la tabla Qr de la base
de datos ParkSmart.

Autor: Equipo ParkSmart
Version: 1.0
Fecha: Junio 2026
---------------------------------------------------------
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, Enum as SqlEnum, ForeignKey, func
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Qr(Base):
    __tablename__ = "Qr"

    idQr: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    idReserva: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "Reserva.idReserva",
            onupdate="CASCADE",
            ondelete="RESTRICT"
        ),
        nullable=False
    )

    codigoQr: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        unique=True
    )

    tokenQr: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True
    )

    fechaGeneracion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp()
    )

    fechaValidezInicio: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    fechaValidezFin: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "GENERADO",
            "USADO",
            "VENCIDO",
            "ANULADO"
        ),
        nullable=False,
        default="GENERADO"
    )

    fechaUso: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    fechaCreacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp()
    )

    fechaActualizacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )