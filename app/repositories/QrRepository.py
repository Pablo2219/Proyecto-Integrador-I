from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.Qr import Qr
from app.models.Reserva import Reserva


class QrRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        consulta = select(Qr)
        return self.db.scalars(consulta).all()

    def listar_por_reserva(self, idReserva: int):
        consulta = select(Qr).where(
            Qr.idReserva == idReserva
        )

        return self.db.scalars(consulta).all()

    def obtener_por_id(self, idQr: int):
        consulta = select(Qr).where(
            Qr.idQr == idQr
        )

        return self.db.scalar(consulta)

    def obtener_por_codigo(self, codigoQr: str):
        consulta = select(Qr).where(
            Qr.codigoQr == codigoQr
        )

        return self.db.scalar(consulta)

    def obtener_activo_por_reserva(self, idReserva: int):
        consulta = select(Qr).where(
            Qr.idReserva == idReserva,
            Qr.estado == "GENERADO"
        )

        return self.db.scalar(consulta)

    def crear(
        self,
        idReserva: int,
        codigoQr: str,
        tokenQr: str,
        fechaValidezInicio,
        fechaValidezFin
    ):
        qr = Qr(
            idReserva=idReserva,
            codigoQr=codigoQr,
            tokenQr=tokenQr,
            fechaValidezInicio=fechaValidezInicio,
            fechaValidezFin=fechaValidezFin,
            estado="GENERADO"
        )

        self.db.add(qr)
        self.db.commit()
        self.db.refresh(qr)

        return qr

    def marcar_usado(self, qr: Qr):
        qr.estado = "USADO"
        qr.fechaUso = datetime.now()

        reserva = self.db.get(Reserva, qr.idReserva)

        if reserva is not None:
            reserva.estado = "UTILIZADA"

        self.db.commit()
        self.db.refresh(qr)

        return qr

    def marcar_vencido(self, qr: Qr):
        qr.estado = "VENCIDO"

        self.db.commit()
        self.db.refresh(qr)

        return qr

    def anular(self, qr: Qr):
        qr.estado = "ANULADO"

        self.db.commit()
        self.db.refresh(qr)

        return qr