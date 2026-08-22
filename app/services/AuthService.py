from sqlalchemy.orm import Session

from app.config.Security import (
    TokenError,
    create_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.config.Settings import settings
from app.repositories.ClienteRepository import ClienteRepository
from app.repositories.RolRepository import RolRepository
from app.repositories.UsuarioRepository import UsuarioRepository
from app.schemas.auth.AuthResponse import AuthResponse
from app.schemas.auth.PasswordChangeRequest import PasswordChangeRequest
from app.schemas.auth.PasswordRecoveryRequest import PasswordRecoveryRequest
from app.schemas.auth.PasswordRecoveryResponse import PasswordRecoveryResponse
from app.schemas.auth.PasswordResetRequest import PasswordResetRequest
from app.schemas.usuario.UsuarioResponse import UsuarioResponse
from app.services.NotificationGateway import NotificationGateway


class AuthService:
    def __init__(self, db: Session):
        self.usuario_repository = UsuarioRepository(db)
        self.rol_repository = RolRepository(db)
        self.cliente_repository = ClienteRepository(db)
        self.gateway = NotificationGateway()

    def usuario_response(self, usuario) -> UsuarioResponse:
        rol = self.rol_repository.obtener_por_id(usuario.idRol)
        return UsuarioResponse(
            idUsuario=usuario.idUsuario,
            idRol=usuario.idRol,
            idCliente=usuario.idCliente,
            nombreUsuario=usuario.nombreUsuario,
            correoElectronico=usuario.correoElectronico,
            rol=rol.nombreRol if rol else "SIN_ROL",
            estado=usuario.estado,
            ultimoAcceso=usuario.ultimoAcceso,
            fechaCreacion=usuario.fechaCreacion,
            fechaActualizacion=usuario.fechaActualizacion,
        )

    def login(self, identificador: str, contrasena: str) -> AuthResponse:
        usuario = self.usuario_repository.obtener_por_identificador(identificador.strip())
        if usuario is None or not verify_password(contrasena, usuario.contrasenaHash):
            raise ValueError("Usuario o contraseña incorrectos.")
        if usuario.estado != "ACTIVO":
            raise ValueError("La cuenta no está activa.")

        rol = self.rol_repository.obtener_por_id(usuario.idRol)
        if rol is None or rol.estado != "ACTIVO":
            raise ValueError("El rol de la cuenta no está disponible.")

        self.usuario_repository.registrar_acceso(usuario)
        token = create_token(
            str(usuario.idUsuario),
            "access",
            settings.ACCESS_TOKEN_MINUTES,
            role=rol.nombreRol,
            client_id=usuario.idCliente,
        )
        return AuthResponse(
            accessToken=token,
            expiresIn=settings.ACCESS_TOKEN_MINUTES * 60,
            usuario=self.usuario_response(usuario),
        )

    def solicitar_restauracion(self, datos: PasswordRecoveryRequest) -> PasswordRecoveryResponse:
        usuario = self.usuario_repository.obtener_por_identificador(datos.usuarioOCorreo.strip())
        respuesta_generica = "Si la cuenta existe, se enviaron instrucciones para restablecer la contraseña."
        if usuario is None or usuario.estado != "ACTIVO":
            return PasswordRecoveryResponse(mensaje=respuesta_generica, canal=datos.canal)

        destinatario = usuario.correoElectronico
        if datos.canal in ["SMS", "WHATSAPP"]:
            cliente = self.cliente_repository.obtener_por_id(usuario.idCliente) if usuario.idCliente else None
            if cliente is None:
                raise ValueError("La cuenta no tiene un teléfono de cliente asociado.")
            destinatario = cliente.telefono
            solo_digitos = "".join(caracter for caracter in destinatario if caracter.isdigit())
            if len(solo_digitos) == 8:
                destinatario = f"{settings.DEFAULT_PHONE_COUNTRY_CODE}{solo_digitos}"

        token = create_token(
            str(usuario.idUsuario),
            "password_reset",
            settings.RESET_TOKEN_MINUTES,
        )
        enlace = f"{settings.FRONTEND_URL}?reset_token={token}"
        resultado = self.gateway.send(
            datos.canal,
            destinatario,
            "Restablecer contraseña de ParkSmart",
            f"Usá este enlace para crear una nueva contraseña: {enlace}",
        )
        if not resultado.success:
            raise ValueError(resultado.detail)

        return PasswordRecoveryResponse(
            mensaje=respuesta_generica,
            canal=datos.canal,
            tokenRestablecimiento=token if settings.AUTH_DEBUG_RESET_TOKEN else None,
        )

    def restablecer(self, datos: PasswordResetRequest):
        try:
            payload = decode_token(datos.token, "password_reset")
        except TokenError as error:
            raise ValueError(str(error)) from error
        usuario = self.usuario_repository.obtener_por_id(int(payload["sub"]))
        if usuario is None or usuario.estado != "ACTIVO":
            raise ValueError("La cuenta ya no está disponible.")
        usuario.contrasenaHash = hash_password(datos.nuevaContrasena)
        self.usuario_repository.guardar(usuario)
        return {"mensaje": "Contraseña restablecida correctamente."}

    def cambiar_contrasena(self, usuario, datos: PasswordChangeRequest):
        if not verify_password(datos.contrasenaActual, usuario.contrasenaHash):
            raise ValueError("La contraseña actual no es correcta.")
        if datos.contrasenaActual == datos.nuevaContrasena:
            raise ValueError("La nueva contraseña debe ser diferente.")
        usuario.contrasenaHash = hash_password(datos.nuevaContrasena)
        self.usuario_repository.guardar(usuario)
        return {"mensaje": "Contraseña actualizada correctamente."}
