from datetime import datetime

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.Usuario import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        return self.db.scalars(select(Usuario).order_by(Usuario.idUsuario)).all()

    def obtener_por_id(self, idUsuario: int):
        return self.db.scalar(select(Usuario).where(Usuario.idUsuario == idUsuario))

    def obtener_por_nombre(self, nombreUsuario: str):
        return self.db.scalar(
            select(Usuario).where(Usuario.nombreUsuario == nombreUsuario)
        )

    def obtener_por_correo(self, correoElectronico: str):
        return self.db.scalar(
            select(Usuario).where(Usuario.correoElectronico == correoElectronico)
        )

    def obtener_por_identificador(self, identificador: str):
        return self.db.scalar(
            select(Usuario).where(
                or_(
                    Usuario.nombreUsuario == identificador,
                    Usuario.correoElectronico == identificador,
                )
            )
        )

    def crear(self, usuario: Usuario):
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def guardar(self, usuario: Usuario):
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def registrar_acceso(self, usuario: Usuario):
        usuario.ultimoAcceso = datetime.now()
        return self.guardar(usuario)
