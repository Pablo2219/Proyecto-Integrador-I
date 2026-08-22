from sqlalchemy import text
from sqlalchemy.engine import Engine

from app.config.Security import hash_password
from app.config.Settings import settings


def _column_exists(connection, table: str, column: str) -> bool:
    result = connection.execute(
        text(
            """
            SELECT COUNT(*)
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table_name
              AND COLUMN_NAME = :column_name
            """
        ),
        {"table_name": table, "column_name": column},
    ).scalar_one()
    return bool(result)


def _constraint_exists(connection, table: str, constraint: str) -> bool:
    result = connection.execute(
        text(
            """
            SELECT COUNT(*)
            FROM information_schema.TABLE_CONSTRAINTS
            WHERE CONSTRAINT_SCHEMA = DATABASE()
              AND TABLE_NAME = :table_name
              AND CONSTRAINT_NAME = :constraint_name
            """
        ),
        {"table_name": table, "constraint_name": constraint},
    ).scalar_one()
    return bool(result)


def ensure_schema(engine: Engine) -> None:
    """Keep an existing development database compatible with the current app."""
    with engine.begin() as connection:
        for nombre, descripcion in (
            ("ADMINISTRADOR", "Administrador del sistema ParkSmart."),
            ("CLIENTE", "Cliente que reserva espacios de parqueo."),
            ("PROVEEDOR", "Proveedor que publica sectores y espacios de parqueo."),
        ):
            connection.execute(
                text(
                    "INSERT INTO Rol (nombreRol, descripcion, estado) "
                    "SELECT :nombre, :descripcion, 'ACTIVO' "
                    "WHERE NOT EXISTS (SELECT 1 FROM Rol WHERE nombreRol=:nombre)"
                ),
                {"nombre": nombre, "descripcion": descripcion},
            )

        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS Proveedor (
                    idProveedor BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                    idUsuario BIGINT UNSIGNED NULL,
                    nombreComercial VARCHAR(120) NOT NULL,
                    identificacionFiscal VARCHAR(30) NULL,
                    telefono VARCHAR(20) NOT NULL,
                    correoElectronico VARCHAR(120) NOT NULL,
                    direccion VARCHAR(250) NULL,
                    estado ENUM('PENDIENTE','ACTIVO','INACTIVO','SUSPENDIDO') NOT NULL DEFAULT 'PENDIENTE',
                    fechaCreacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    fechaActualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    PRIMARY KEY (idProveedor),
                    UNIQUE KEY uk_proveedor_usuario (idUsuario),
                    UNIQUE KEY uk_proveedor_fiscal (identificacionFiscal)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
        )

        if not _column_exists(connection, "Usuario", "idProveedor"):
            connection.execute(text("ALTER TABLE Usuario ADD COLUMN idProveedor BIGINT UNSIGNED NULL"))
        if not _constraint_exists(connection, "Usuario", "uk_usuario_proveedor"):
            try:
                connection.execute(text("ALTER TABLE Usuario ADD UNIQUE KEY uk_usuario_proveedor (idProveedor)"))
            except Exception:
                pass
        if not _constraint_exists(connection, "Usuario", "fk_usuario_proveedor"):
            try:
                connection.execute(
                    text(
                        "ALTER TABLE Usuario ADD CONSTRAINT fk_usuario_proveedor "
                        "FOREIGN KEY (idProveedor) REFERENCES Proveedor(idProveedor) "
                        "ON DELETE SET NULL ON UPDATE CASCADE"
                    )
                )
            except Exception:
                pass

        for column, definition in (
            ("idProveedor", "BIGINT UNSIGNED NULL"),
            ("latitud", "DECIMAL(10,7) NULL"),
            ("longitud", "DECIMAL(10,7) NULL"),
            ("precioHora", "DECIMAL(10,2) NOT NULL DEFAULT 0"),
        ):
            if not _column_exists(connection, "Sector", column):
                connection.execute(text(f"ALTER TABLE Sector ADD COLUMN {column} {definition}"))

        if not _constraint_exists(connection, "Sector", "fk_sector_proveedor"):
            try:
                connection.execute(
                    text(
                        "ALTER TABLE Sector ADD CONSTRAINT fk_sector_proveedor "
                        "FOREIGN KEY (idProveedor) REFERENCES Proveedor(idProveedor) "
                        "ON DELETE RESTRICT ON UPDATE CASCADE"
                    )
                )
            except Exception:
                pass

        for column in ("latitud", "longitud"):
            if not _column_exists(connection, "Espacio", column):
                connection.execute(text(f"ALTER TABLE Espacio ADD COLUMN {column} DECIMAL(10,7) NULL"))

        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS consentimiento_privacidad (
                    idConsentimiento BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                    idUsuario BIGINT UNSIGNED NOT NULL,
                    versionAviso VARCHAR(20) NOT NULL,
                    finalidad VARCHAR(500) NOT NULL,
                    aceptado TINYINT(1) NOT NULL DEFAULT 1,
                    fechaAceptacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (idConsentimiento),
                    KEY ix_consentimiento_usuario (idUsuario)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
        )
        if not _constraint_exists(connection, "consentimiento_privacidad", "fk_consentimiento_usuario"):
            try:
                connection.execute(
                    text(
                        "ALTER TABLE consentimiento_privacidad ADD CONSTRAINT fk_consentimiento_usuario "
                        "FOREIGN KEY (idUsuario) REFERENCES Usuario(idUsuario) "
                        "ON DELETE RESTRICT ON UPDATE CASCADE"
                    )
                )
            except Exception:
                pass

        admin_role = connection.execute(
            text("SELECT idRol FROM Rol WHERE nombreRol='ADMINISTRADOR' LIMIT 1")
        ).scalar_one()
        existing_admin = connection.execute(
            text(
                "SELECT idUsuario FROM Usuario "
                "WHERE nombreUsuario=:username OR correoElectronico=:email LIMIT 1"
            ),
            {"username": settings.ADMIN_USERNAME, "email": settings.ADMIN_EMAIL.lower()},
        ).scalar()

        if existing_admin is None:
            connection.execute(
                text(
                    "INSERT INTO Usuario "
                    "(idRol,idCliente,idProveedor,nombreUsuario,correoElectronico,contrasenaHash,estado) "
                    "VALUES (:rol,NULL,NULL,:username,:email,:password,'ACTIVO')"
                ),
                {
                    "rol": admin_role,
                    "username": settings.ADMIN_USERNAME,
                    "email": settings.ADMIN_EMAIL.lower(),
                    "password": hash_password(settings.ADMIN_PASSWORD),
                },
            )
        else:
            values = {
                "rol": admin_role,
                "id": existing_admin,
                "estado": "ACTIVO",
            }
            password_sql = ", contrasenaHash=:password" if settings.ADMIN_RESET_PASSWORD_ON_STARTUP else ""
            if settings.ADMIN_RESET_PASSWORD_ON_STARTUP:
                values["password"] = hash_password(settings.ADMIN_PASSWORD)
            connection.execute(
                text(
                    "UPDATE Usuario SET idRol=:rol, estado=:estado" + password_sql + " WHERE idUsuario=:id"
                ),
                values,
            )


def startup_check(engine: Engine) -> None:
    try:
        ensure_schema(engine)
    except Exception as error:
        raise RuntimeError(
            "No se pudo preparar la base de datos de ParkSmart. "
            "Verifique que MySQL esté disponible y que DATABASE_URL sea correcto. "
            f"Detalle: {error}"
        ) from error
