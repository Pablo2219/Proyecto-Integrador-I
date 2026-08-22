from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, String, func
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Ocupacion(Base):
    __tablename__ = "Ocupacion"

    idOcupacion: Mapped[int] = mapped_column(
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

    idEspacio: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "Espacio.idEspacio",
            onupdate="CASCADE",
            ondelete="RESTRICT"
        ),
        nullable=False
    )

    fechaEntrada: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp()
    )

    fechaSalida: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "EN_CURSO",
            "FINALIZADA",
            "CANCELADA"
        ),
        nullable=False,
        default="EN_CURSO"
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