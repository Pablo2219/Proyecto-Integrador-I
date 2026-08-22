from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum as SqlEnum, String, func
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Rol(Base):
    __tablename__ = "Rol"

    idRol: Mapped[int] = mapped_column(
        BIGINT(unsigned=True), primary_key=True, autoincrement=True
    )
    nombreRol: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    descripcion: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    estado: Mapped[str] = mapped_column(
        SqlEnum("ACTIVO", "INACTIVO"), nullable=False, default="ACTIVO"
    )
    fechaCreacion: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.current_timestamp()
    )
    fechaActualizacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
