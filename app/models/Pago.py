from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, String, func
from sqlalchemy.dialects.mysql import BIGINT, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Pago(Base):
    __tablename__ = "Pago"

    idPago: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True
    )

    idOcupacion: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "Ocupacion.idOcupacion",
            onupdate="CASCADE",
            ondelete="RESTRICT"
        ),
        nullable=False
    )

    codigoPago: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        unique=True
    )

    montoTotal: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2),
        nullable=False
    )

    metodoPago: Mapped[Optional[str]] = mapped_column(
        SqlEnum(
            "EFECTIVO",
            "TARJETA",
            "SINPE",
            "PASARELA"
        ),
        nullable=True
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "PENDIENTE",
            "PAGADO",
            "VENCIDO",
            "ANULADO"
        ),
        nullable=False,
        default="PENDIENTE"
    )

    fechaGeneracion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp()
    )

    fechaLimitePago: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    fechaPago: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    referenciaTransaccion: Mapped[Optional[str]] = mapped_column(
        String(120),
        nullable=True
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