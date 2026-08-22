from sqlalchemy.orm import Session

from app.repositories.OcupacionRepository import OcupacionRepository
from app.repositories.ReservaRepository import ReservaRepository
from app.schemas.ocupacion.OcupacionCreate import OcupacionCreate
from app.schemas.ocupacion.OcupacionUpdate import OcupacionUpdate


class OcupacionService:

    def __init__(self, db: Session):
        self.ocupacion_repository = OcupacionRepository(db)
        self.reserva_repository = ReservaRepository(db)

    def listar_ocupaciones(self):
        return self.ocupacion_repository.listar()

    def listar_ocupaciones_activas(self):
        return self.ocupacion_repository.listar_activas()

    def listar_ocupaciones_por_reserva(self, idReserva: int):
        reserva = self.reserva_repository.obtener_por_id(idReserva)

        if reserva is None:
            raise ValueError("La reserva no existe.")

        return self.ocupacion_repository.listar_por_reserva(idReserva)

    def obtener_ocupacion(self, idOcupacion: int):
        ocupacion = self.ocupacion_repository.obtener_por_id(idOcupacion)

        if ocupacion is None:
            raise ValueError("La ocupacion no existe.")

        return ocupacion

    def iniciar_ocupacion(self, datos: OcupacionCreate):
        reserva = self.reserva_repository.obtener_por_id(datos.idReserva)

        if reserva is None:
            raise ValueError("La reserva no existe.")

        if reserva.estado not in ["CONFIRMADA", "UTILIZADA"]:
            raise ValueError(
                "Solo se puede iniciar ocupacion para reservas confirmadas o utilizadas."
            )

        ocupacion_activa = self.ocupacion_repository.obtener_activa_por_reserva(
            datos.idReserva
        )

        if ocupacion_activa is not None:
            raise ValueError(
                "Ya existe una ocupacion activa para esta reserva."
            )

        return self.ocupacion_repository.crear(
            datos.idReserva,
            reserva.idEspacio,
            datos.observaciones
        )

    def actualizar_ocupacion(
        self,
        idOcupacion: int,
        datos: OcupacionUpdate
    ):
        ocupacion = self.ocupacion_repository.obtener_por_id(idOcupacion)

        if ocupacion is None:
            raise ValueError("La ocupacion no existe.")

        if ocupacion.estado != "EN_CURSO":
            raise ValueError(
                "Solo se pueden modificar ocupaciones en curso."
            )

        return self.ocupacion_repository.actualizar(ocupacion, datos)

    def finalizar_ocupacion(self, idOcupacion: int):
        ocupacion = self.ocupacion_repository.obtener_por_id(idOcupacion)

        if ocupacion is None:
            raise ValueError("La ocupacion no existe.")

        if ocupacion.estado != "EN_CURSO":
            raise ValueError(
                "Solo se pueden finalizar ocupaciones en curso."
            )

        return self.ocupacion_repository.finalizar(ocupacion)

    def cancelar_ocupacion(self, idOcupacion: int):
        ocupacion = self.ocupacion_repository.obtener_por_id(idOcupacion)

        if ocupacion is None:
            raise ValueError("La ocupacion no existe.")

        if ocupacion.estado != "EN_CURSO":
            raise ValueError(
                "Solo se pueden cancelar ocupaciones en curso."
            )

        return self.ocupacion_repository.cancelar(ocupacion)