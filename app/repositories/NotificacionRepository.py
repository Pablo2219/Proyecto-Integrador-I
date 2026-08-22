from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.Notificacion import Notificacion
from app.schemas.notificacion.NotificacionCreate import NotificacionCreate
from app.schemas.notificacion.NotificacionUpdate import NotificacionUpdate


class NotificacionRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        return self.db.scalars(
            select(Notificacion).order_by(Notificacion.fechaCreacion.desc())
        ).all()

    def listar_pendientes(self):
        return self.db.scalars(
            select(Notificacion)
            .where(Notificacion.estado == "PENDIENTE")
            .order_by(Notificacion.fechaCreacion.desc())
        ).all()

    def listar_por_cliente(self, idCliente: int):
        return self.db.scalars(
            select(Notificacion)
            .where(Notificacion.idCliente == idCliente)
            .order_by(Notificacion.fechaCreacion.desc())
        ).all()

    def obtener_por_id(self, idNotificacion: int):
        return self.db.scalar(
            select(Notificacion).where(Notificacion.idNotificacion == idNotificacion)
        )

    def crear(self, datos: NotificacionCreate, destinatario: str):
        valores = datos.model_dump(exclude={"enviarAhora"})
        valores["destinatario"] = destinatario
        notificacion = Notificacion(**valores)
        self.db.add(notificacion)
        self.db.commit()
        self.db.refresh(notificacion)
        return notificacion

    def actualizar(self, notificacion: Notificacion, datos: NotificacionUpdate):
        for campo, valor in datos.model_dump(exclude_unset=True).items():
            setattr(notificacion, campo, valor)
        self.db.commit()
        self.db.refresh(notificacion)
        return notificacion

    def marcar_enviada(self, notificacion: Notificacion, observacion: str | None = None):
        notificacion.estado = "ENVIADA"
        notificacion.fechaEnvio = datetime.now()
        if observacion:
            notificacion.observaciones = observacion[:250]
        self.db.commit()
        self.db.refresh(notificacion)
        return notificacion

    def marcar_leida(self, notificacion: Notificacion):
        notificacion.estado = "LEIDA"
        notificacion.fechaLectura = datetime.now()
        self.db.commit()
        self.db.refresh(notificacion)
        return notificacion

    def marcar_fallida(self, notificacion: Notificacion, observacion: str | None = None):
        notificacion.estado = "FALLIDA"
        if observacion:
            notificacion.observaciones = observacion[:250]
        self.db.commit()
        self.db.refresh(notificacion)
        return notificacion

    def anular(self, notificacion: Notificacion):
        notificacion.estado = "ANULADA"
        self.db.commit()
        self.db.refresh(notificacion)
        return notificacion
