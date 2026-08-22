"""
---------------------------------------------------------
Proyecto: ParkSmart - Sistema de Parqueo Inteligente
Archivo: Espacio.py

Descripcion:
Modelo ORM que representa la tabla Espacio de la base
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


class Espacio(Base):
    __tablename__ = "Espacio"

    idEspacio: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    idSector: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "Sector.idSector",
            onupdate="CASCADE",
            ondelete="RESTRICT"
        ),
        nullable=False
    )

    codigoEspacio: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True
    )

    tipoEspacio: Mapped[str] = mapped_column(
        SqlEnum(
            "REGULAR",
            "MOTOCICLETA",
            "DISCAPACIDAD",
            "ELECTRICO",
            "VIP"
        ),
        nullable=False,
        default="REGULAR"
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "DISPONIBLE",
            "OCUPADO",
            "RESERVADO",
            "MANTENIMIENTO",
            "INACTIVO"
        ),
        nullable=False,
        default="DISPONIBLE"
    )

    descripcion: Mapped[Optional[str]] = mapped_column(
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