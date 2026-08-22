from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, Enum as SqlEnum, func
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Cliente(Base):
    __tablename__ = "Cliente"

    idCliente: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    identificacion: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True
    )

    nombre: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    primerApellido: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    segundoApellido: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )

    telefono: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    correoElectronico: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True
    )

    provincia: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )

    canton: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )

    distrito: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )

    direccionExacta: Mapped[Optional[str]] = mapped_column(
        String(250),
        nullable=True
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "ACTIVO",
            "INACTIVO",
            "SUSPENDIDO"
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