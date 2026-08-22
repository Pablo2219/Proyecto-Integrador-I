"""
---------------------------------------------------------
Proyecto: ParkSmart - Sistema de Parqueo Inteligente
Archivo: Reserva.py

Descripcion:
Modelo ORM que representa la tabla Reserva de la base
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


class Reserva(Base):
    __tablename__ = "Reserva"

    idReserva: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    idCliente: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "Cliente.idCliente",
            onupdate="CASCADE",
            ondelete="RESTRICT"
        ),
        nullable=False
    )

    idVehiculo: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "Vehiculo.idVehiculo",
            onupdate="CASCADE",
            ondelete="RESTRICT"
        ),
        nullable=False
    )

    idEspacio: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "Espacio.idEspacio",
            onupdate="CASCADE",
            ondelete="RESTRICT"
        ),
        nullable=False
    )

    codigoReserva: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True
    )

    fechaInicioReserva: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    fechaFinReserva: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "PENDIENTE",
            "CONFIRMADA",
            "CANCELADA",
            "VENCIDA",
            "UTILIZADA"
        ),
        nullable=False,
        default="PENDIENTE"
    )

    observaciones: Mapped[Optional[str]] = mapped_column(
        String(250),
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