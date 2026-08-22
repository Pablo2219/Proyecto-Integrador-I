from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.Espacio import Espacio
from app.models.Ocupacion import Ocupacion
from app.models.Reserva import Reserva
from app.schemas.ocupacion.OcupacionUpdate import OcupacionUpdate


class OcupacionRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        consulta = select(Ocupacion)
        return self.db.scalars(consulta).all()

    def listar_activas(self):
        consulta = select(Ocupacion).where(
            Ocupacion.estado == "EN_CURSO"
        )

        return self.db.scalars(consulta).all()

    def listar_por_reserva(self, idReserva: int):
        consulta = select(Ocupacion).where(
            Ocupacion.idReserva == idReserva
        )

        return self.db.scalars(consulta).all()

    def obtener_por_id(self, idOcupacion: int):
        consulta = select(Ocupacion).where(
            Ocupacion.idOcupacion == idOcupacion
        )

        return self.db.scalar(consulta)

    def obtener_activa_por_reserva(self, idReserva: int):
        consulta = select(Ocupacion).where(
            Ocupacion.idReserva == idReserva,
            Ocupacion.estado == "EN_CURSO"
        )

        return self.db.scalar(consulta)

    def crear(self, idReserva: int, idEspacio: int, observaciones: str | None):
        ocupacion = Ocupacion(
            idReserva=idReserva,
            idEspacio=idEspacio,
            estado="EN_CURSO",
            observaciones=observaciones
        )

        espacio = self.db.get(Espacio, idEspacio)

        if espacio is not None:
            espacio.estado = "OCUPADO"

        reserva = self.db.get(Reserva, idReserva)

        if reserva is not None:
            reserva.estado = "UTILIZADA"

        self.db.add(ocupacion)
        self.db.commit()
        self.db.refresh(ocupacion)

        return ocupacion

    def actualizar(self, ocupacion: Ocupacion, datos: OcupacionUpdate):
        datos_actualizados = datos.model_dump(exclude_unset=True)

        for campo, valor in datos_actualizados.items():
            setattr(ocupacion, campo, valor)

        self.db.commit()
        self.db.refresh(ocupacion)

        return ocupacion

    def finalizar(self, ocupacion: Ocupacion):
        ocupacion.estado = "FINALIZADA"
        ocupacion.fechaSalida = datetime.now()

        espacio = self.db.get(Espacio, ocupacion.idEspacio)

        if espacio is not None:
            espacio.estado = "DISPONIBLE"

        self.db.commit()
        self.db.refresh(ocupacion)

        return ocupacion

    def cancelar(self, ocupacion: Ocupacion):
        ocupacion.estado = "CANCELADA"

        espacio = self.db.get(Espacio, ocupacion.idEspacio)

        if espacio is not None:
            espacio.estado = "DISPONIBLE"

        self.db.commit()
        self.db.refresh(ocupacion)

        return ocupacion