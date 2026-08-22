"""
---------------------------------------------------------
Proyecto: ParkSmart - Sistema de Parqueo Inteligente
Archivo: Vehiculo.py

Descripcion:
Modelo ORM que representa la tabla Vehiculo de la base
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


class Vehiculo(Base):
    __tablename__ = "Vehiculo"

    idVehiculo: Mapped[int] = mapped_column(
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

    placa: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True
    )

    marca: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )

    modelo: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )

    color: Mapped[Optional[str]] = mapped_column(
        String(30),
        nullable=True
    )

    tipoVehiculo: Mapped[str] = mapped_column(
        SqlEnum(
            "AUTOMOVIL",
            "MOTOCICLETA",
            "CAMIONETA",
            "OTRO"
        ),
        nullable=False,
        default="AUTOMOVIL"
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "ACTIVO",
            "INACTIVO"
        ),
        nullable=False,
        default="ACTIVO"
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