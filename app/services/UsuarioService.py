from sqlalchemy.orm import Session

from app.config.Security import hash_password
from app.models.Usuario import Usuario
from app.repositories.ClienteRepository import ClienteRepository
from app.repositories.RolRepository import RolRepository
from app.repositories.UsuarioRepository import UsuarioRepository
from app.schemas.usuario.UsuarioCreate import UsuarioCreate
from app.schemas.usuario.UsuarioResponse import UsuarioResponse
from app.schemas.usuario.UsuarioUpdate import UsuarioUpdate


class UsuarioService:
    def __init__(self, db: Session):
        self.usuario_repository = UsuarioRepository(db)
        self.rol_repository = RolRepository(db)
        self.cliente_repository = ClienteRepository(db)

    def _respuesta(self, usuario: Usuario) -> UsuarioResponse:
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

    def listar_usuarios(self):
        return [self._respuesta(usuario) for usuario in self.usuario_repository.listar()]

    def obtener_usuario(self, idUsuario: int):
        usuario = self.usuario_repository.obtener_por_id(idUsuario)
        if usuario is None:
            raise ValueError("El usuario no existe.")
        return self._respuesta(usuario)

    def crear_usuario(self, datos: UsuarioCreate):
        if self.usuario_repository.obtener_por_nombre(datos.nombreUsuario):
            raise ValueError("El nombre de usuario ya está registrado.")
        if self.usuario_repository.obtener_por_correo(str(datos.correoElectronico)):
            raise ValueError("El correo electrónico ya está registrado.")

        rol = self.rol_repository.obtener_por_nombre(datos.rol)
        if rol is None or rol.estado != "ACTIVO":
            raise ValueError("El rol indicado no está disponible.")

        if datos.rol == "CLIENTE":
            if datos.idCliente is None:
                raise ValueError("Un usuario CLIENTE debe estar asociado a un cliente.")
            if self.cliente_repository.obtener_por_id(datos.idCliente) is None:
                raise ValueError("El cliente asociado no existe.")
        elif datos.idCliente is not None and self.cliente_repository.obtener_por_id(datos.idCliente) is None:
            raise ValueError("El cliente asociado no existe.")

        usuario = Usuario(
            idRol=rol.idRol,
            idCliente=datos.idCliente,
            nombreUsuario=datos.nombreUsuario.strip(),
            correoElectronico=str(datos.correoElectronico).lower(),
            contrasenaHash=hash_password(datos.contrasena),
            estado="ACTIVO",
        )
        return self._respuesta(self.usuario_repository.crear(usuario))

    def actualizar_usuario(self, idUsuario: int, datos: UsuarioUpdate):
        usuario = self.usuario_repository.obtener_por_id(idUsuario)
        if usuario is None:
            raise ValueError("El usuario no existe.")

        if datos.correoElectronico is not None:
            existente = self.usuario_repository.obtener_por_correo(str(datos.correoElectronico))
            if existente and existente.idUsuario != idUsuario:
                raise ValueError("El correo electrónico ya está registrado.")
            usuario.correoElectronico = str(datos.correoElectronico).lower()

        if datos.rol is not None:
            rol = self.rol_repository.obtener_por_nombre(datos.rol)
            if rol is None:
                raise ValueError("El rol indicado no existe.")
            usuario.idRol = rol.idRol

        if "idCliente" in datos.model_fields_set:
            if datos.idCliente is not None and self.cliente_repository.obtener_por_id(datos.idCliente) is None:
                raise ValueError("El cliente asociado no existe.")
            usuario.idCliente = datos.idCliente

        if datos.estado is not None:
            usuario.estado = datos.estado

        rol_actual = self.rol_repository.obtener_por_id(usuario.idRol)
        if rol_actual and rol_actual.nombreRol == "CLIENTE" and usuario.idCliente is None:
            raise ValueError("Un usuario CLIENTE debe conservar un cliente asociado.")

        return self._respuesta(self.usuario_repository.guardar(usuario))

    def eliminar_usuario(self, idUsuario: int):
        usuario = self.usuario_repository.obtener_por_id(idUsuario)
        if usuario is None:
            raise ValueError("El usuario no existe.")
        usuario.estado = "INACTIVO"
        return self._respuesta(self.usuario_repository.guardar(usuario))
