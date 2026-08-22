from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, String, func
from sqlalchemy.dialects.mysql import BIGINT, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Deuda(Base):
    __tablename__ = "Deuda"

    idDeuda: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    idPago: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "Pago.idPago",
            onupdate="CASCADE",
            ondelete="RESTRICT"
        ),
        nullable=False
    )

    codigoDeuda: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        unique=True
    )

    montoDeuda: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2),
        nullable=False
    )

    fechaGeneracion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp()
    )

    fechaLimite: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "PENDIENTE",
            "PAGADA",
            "VENCIDA",
            "ANULADA"
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