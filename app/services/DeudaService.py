from datetime import datetime

from sqlalchemy.orm import Session

from app.repositories.DeudaRepository import DeudaRepository
from app.repositories.PagoRepository import PagoRepository
from app.schemas.deuda.DeudaCreate import DeudaCreate
from app.schemas.deuda.DeudaUpdate import DeudaUpdate


class DeudaService:

    def __init__(self, db: Session):
        self.deuda_repository = DeudaRepository(db)
        self.pago_repository = PagoRepository(db)

    def listar_deudas(self):
        return self.deuda_repository.listar()

    def listar_deudas_pendientes(self):
        return self.deuda_repository.listar_pendientes()

    def listar_deudas_vencidas(self):
        return self.deuda_repository.listar_vencidas()

    def listar_deudas_por_pago(self, idPago: int):
        pago = self.pago_repository.obtener_por_id(idPago)

        if pago is None:
            raise ValueError("El pago no existe.")

        return self.deuda_repository.listar_por_pago(idPago)

    def obtener_deuda(self, idDeuda: int):
        deuda = self.deuda_repository.obtener_por_id(idDeuda)

        if deuda is None:
            raise ValueError("La deuda no existe.")

        return deuda

    def crear_deuda(self, datos: DeudaCreate):
        pago = self.pago_repository.obtener_por_id(datos.idPago)

        if pago is None:
            raise ValueError("El pago no existe.")

        if pago.estado == "PAGADO":
            raise ValueError("No se puede generar deuda para un pago pagado.")

        if pago.estado == "ANULADO":
            raise ValueError("No se puede generar deuda para un pago anulado.")

        if pago.estado == "PENDIENTE" and datetime.now() <= pago.fechaLimitePago:
            raise ValueError(
                "El pago todavia esta dentro del plazo de 24 horas."
            )

        if pago.estado == "PENDIENTE" and datetime.now() > pago.fechaLimitePago:
            self.pago_repository.marcar_vencido(pago)

        deuda_existente = self.deuda_repository.obtener_activa_por_pago(
            datos.idPago
        )

        if deuda_existente is not None:
            raise ValueError(
                "Ya existe una deuda activa para este pago."
            )

        codigo_deuda = self.generar_codigo_deuda()

        return self.deuda_repository.crear(
            datos.idPago,
            codigo_deuda,
            pago.montoTotal,
            datos.observaciones
        )

    def actualizar_deuda(self, idDeuda: int, datos: DeudaUpdate):
        deuda = self.deuda_repository.obtener_por_id(idDeuda)

        if deuda is None:
            raise ValueError("La deuda no existe.")

        if deuda.estado == "PAGADA":
            raise ValueError("No se puede modificar una deuda pagada.")

        return self.deuda_repository.actualizar(deuda, datos)

    def pagar_deuda(self, idDeuda: int):
        deuda = self.deuda_repository.obtener_por_id(idDeuda)

        if deuda is None:
            raise ValueError("La deuda no existe.")

        if deuda.estado != "PENDIENTE" and deuda.estado != "VENCIDA":
            raise ValueError("Solo se pueden pagar deudas pendientes o vencidas.")

        return self.deuda_repository.pagar(deuda)

    def vencer_deuda(self, idDeuda: int):
        deuda = self.deuda_repository.obtener_por_id(idDeuda)

        if deuda is None:
            raise ValueError("La deuda no existe.")

        if deuda.estado != "PENDIENTE":
            raise ValueError("Solo se pueden vencer deudas pendientes.")

        return self.deuda_repository.marcar_vencida(deuda)

    def anular_deuda(self, idDeuda: int):
        deuda = self.deuda_repository.obtener_por_id(idDeuda)

        if deuda is None:
            raise ValueError("La deuda no existe.")

        if deuda.estado == "PAGADA":
            raise ValueError("No se puede anular una deuda pagada.")

        return self.deuda_repository.anular(deuda)

    def generar_codigo_deuda(self):
        fecha = datetime.now().strftime("%Y%m%d%H%M%S%f")
        return f"DEU-{fecha}"