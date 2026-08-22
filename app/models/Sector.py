"""
---------------------------------------------------------
Proyecto: ParkSmart - Sistema de Parqueo Inteligente
Archivo: Sector.py

Descripcion:
Modelo ORM que representa la tabla Sector de la base
de datos ParkSmart.

Autor: Equipo ParkSmart
Version: 1.0
Fecha: Junio 2026
---------------------------------------------------------
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, Enum as SqlEnum, func
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Sector(Base):
    __tablename__ = "Sector"

    idSector: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    nombreSector: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )

    descripcion: Mapped[Optional[str]] = mapped_column(
        String(250),
        nullable=True
    )

    ubicacion: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "ACTIVO",
            "INACTIVO",
            "MANTENIMIENTO"
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