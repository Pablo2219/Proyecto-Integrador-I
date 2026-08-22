from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, String, func
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column
from app.database.Base import Base
from app.models.Proveedor import Proveedor  # noqa: F401


class Usuario(Base):
    __tablename__ = "Usuario"
    idUsuario: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    idRol: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey("Rol.idRol", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    idCliente: Mapped[Optional[int]] = mapped_column(BIGINT(unsigned=True), ForeignKey("Cliente.idCliente", onupdate="CASCADE", ondelete="SET NULL"), nullable=True)
    idProveedor: Mapped[Optional[int]] = mapped_column(BIGINT(unsigned=True), ForeignKey("Proveedor.idProveedor", onupdate="CASCADE", ondelete="SET NULL"), nullable=True)
    nombreUsuario: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    correoElectronico: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    contrasenaHash: Mapped[str] = mapped_column(String(255), nullable=False)
    estado: Mapped[str] = mapped_column(SqlEnum("ACTIVO", "INACTIVO", "BLOQUEADO"), nullable=False, default="ACTIVO")
    ultimoAcceso: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fechaCreacion: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp())
    fechaActualizacion: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
