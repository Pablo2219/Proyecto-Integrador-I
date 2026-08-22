from sqlalchemy.orm import Session

from app.config.Settings import settings
from app.repositories.ClienteRepository import ClienteRepository
from app.repositories.DeudaRepository import DeudaRepository
from app.repositories.NotificacionRepository import NotificacionRepository
from app.repositories.PagoRepository import PagoRepository
from app.repositories.ReservaRepository import ReservaRepository
from app.schemas.notificacion.NotificacionCreate import NotificacionCreate
from app.schemas.notificacion.NotificacionUpdate import NotificacionUpdate
from app.services.NotificationGateway import NotificationGateway


class NotificacionService:
    def __init__(self, db: Session):
        self.notificacion_repository = NotificacionRepository(db)
        self.cliente_repository = ClienteRepository(db)
        self.reserva_repository = ReservaRepository(db)
        self.pago_repository = PagoRepository(db)
        self.deuda_repository = DeudaRepository(db)
        self.gateway = NotificationGateway()

    def listar_notificaciones(self):
        return self.notificacion_repository.listar()

    def listar_notificaciones_pendientes(self):
        return self.notificacion_repository.listar_pendientes()

    def listar_notificaciones_por_cliente(self, idCliente: int):
        if self.cliente_repository.obtener_por_id(idCliente) is None:
            raise ValueError("El cliente no existe.")
        return self.notificacion_repository.listar_por_cliente(idCliente)

    def obtener_notificacion(self, idNotificacion: int):
        notificacion = self.notificacion_repository.obtener_por_id(idNotificacion)
        if notificacion is None:
            raise ValueError("La notificación no existe.")
        return notificacion

    def _validar_relaciones(self, datos: NotificacionCreate):
        cliente = self.cliente_repository.obtener_por_id(datos.idCliente)
        if cliente is None:
            raise ValueError("El cliente no existe.")
        if datos.idReserva is not None and self.reserva_repository.obtener_por_id(datos.idReserva) is None:
            raise ValueError("La reserva asociada no existe.")
        if datos.idPago is not None and self.pago_repository.obtener_por_id(datos.idPago) is None:
            raise ValueError("El pago asociado no existe.")
        if datos.idDeuda is not None and self.deuda_repository.obtener_por_id(datos.idDeuda) is None:
            raise ValueError("La deuda asociada no existe.")
        return cliente

    def _resolver_destinatario(self, datos: NotificacionCreate, cliente) -> str:
        if datos.destinatario:
            return datos.destinatario.strip()
        if datos.canal == "EMAIL":
            return cliente.correoElectronico
        if datos.canal in ["SMS", "WHATSAPP"]:
            digitos = "".join(caracter for caracter in cliente.telefono if caracter.isdigit())
            return f"{settings.DEFAULT_PHONE_COUNTRY_CODE}{digitos}" if len(digitos) == 8 else f"+{digitos}"
        return f"cliente:{cliente.idCliente}"

    def crear_notificacion(self, datos: NotificacionCreate):
        cliente = self._validar_relaciones(datos)
        destinatario = self._resolver_destinatario(datos, cliente)
        notificacion = self.notificacion_repository.crear(datos, destinatario)
        if datos.enviarAhora:
            return self._despachar(notificacion)
        return notificacion

    def actualizar_notificacion(self, idNotificacion: int, datos: NotificacionUpdate):
        notificacion = self.obtener_notificacion(idNotificacion)
        if notificacion.estado in ["ENVIADA", "LEIDA", "ANULADA"]:
            raise ValueError("No se puede modificar una notificación enviada, leída o anulada.")
        return self.notificacion_repository.actualizar(notificacion, datos)

    def _despachar(self, notificacion):
        resultado = self.gateway.send(
            notificacion.canal,
            notificacion.destinatario or "sin-destinatario",
            notificacion.titulo,
            notificacion.mensaje,
        )
        if resultado.success:
            return self.notificacion_repository.marcar_enviada(notificacion, resultado.detail)
        return self.notificacion_repository.marcar_fallida(notificacion, resultado.detail)

    def enviar_notificacion(self, idNotificacion: int):
        notificacion = self.obtener_notificacion(idNotificacion)
        if notificacion.estado not in ["PENDIENTE", "FALLIDA"]:
            raise ValueError("Solo se pueden enviar notificaciones pendientes o fallidas.")
        return self._despachar(notificacion)

    def leer_notificacion(self, idNotificacion: int):
        notificacion = self.obtener_notificacion(idNotificacion)
        if notificacion.estado not in ["ENVIADA", "PENDIENTE"]:
            raise ValueError("Solo se pueden marcar como leídas notificaciones pendientes o enviadas.")
        return self.notificacion_repository.marcar_leida(notificacion)

    def fallar_notificacion(self, idNotificacion: int):
        notificacion = self.obtener_notificacion(idNotificacion)
        if notificacion.estado not in ["PENDIENTE", "ENVIADA"]:
            raise ValueError("Solo se pueden marcar como fallidas notificaciones pendientes o enviadas.")
        return self.notificacion_repository.marcar_fallida(notificacion, "Marcada manualmente como fallida.")

    def anular_notificacion(self, idNotificacion: int):
        notificacion = self.obtener_notificacion(idNotificacion)
        if notificacion.estado == "LEIDA":
            raise ValueError("No se puede anular una notificación leída.")
        return self.notificacion_repository.anular(notificacion)
