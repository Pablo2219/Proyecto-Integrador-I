from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.Rol import Rol


class RolRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_activos(self):
        return self.db.scalars(select(Rol).where(Rol.estado == "ACTIVO")).all()

    def obtener_por_id(self, idRol: int):
        return self.db.scalar(select(Rol).where(Rol.idRol == idRol))

    def obtener_por_nombre(self, nombreRol: str):
        return self.db.scalar(
            select(Rol).where(Rol.nombreRol == nombreRol.upper())
        )
