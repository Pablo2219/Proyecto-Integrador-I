from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column
from app.database.Base import Base

class Proveedor(Base):
    __tablename__ = "Proveedor"
    idProveedor: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    nombreComercial: Mapped[str] = mapped_column(String(120), nullable=False)
    identificacionFiscal: Mapped[Optional[str]] = mapped_column(String(30), nullable=True, unique=True)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)
    correoElectronico: Mapped[str] = mapped_column(String(120), nullable=False)
    direccion: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="PENDIENTE")
    fechaCreacion: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())
    fechaActualizacion: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
