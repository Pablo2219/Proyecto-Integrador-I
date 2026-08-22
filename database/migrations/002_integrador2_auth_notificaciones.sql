USE parksmart;

ALTER TABLE Notificacion
    MODIFY tipoNotificacion ENUM('RESERVA','QR','PAGO','DEUDA','SISTEMA') NOT NULL,
    MODIFY estado ENUM('PENDIENTE','ENVIADA','FALLIDA','LEIDA','ANULADA') NOT NULL DEFAULT 'PENDIENTE';

SET @fk_deuda_exists = (
    SELECT COUNT(*)
    FROM information_schema.TABLE_CONSTRAINTS
    WHERE CONSTRAINT_SCHEMA = DATABASE()
      AND TABLE_NAME = 'Notificacion'
      AND CONSTRAINT_NAME = 'FK_Notificacion_Deuda'
);
SET @fk_deuda_sql = IF(
    @fk_deuda_exists = 0,
    'ALTER TABLE Notificacion ADD CONSTRAINT FK_Notificacion_Deuda FOREIGN KEY (idDeuda) REFERENCES Deuda(idDeuda) ON DELETE SET NULL ON UPDATE CASCADE',
    'SELECT 1'
);
PREPARE fk_stmt FROM @fk_deuda_sql;
EXECUTE fk_stmt;
DEALLOCATE PREPARE fk_stmt;

INSERT INTO Usuario
    (idRol, idCliente, nombreUsuario, correoElectronico, contrasenaHash, estado)
SELECT 1, NULL, 'admin', 'admin@parksmart.com',
       'pbkdf2_sha256$310000$1d0292956eccceca6dc2337fc30f269a$81af3cfe40ce6dc8402cf4f9aed8303a64d2566bb4413dc37be316a387fc4f09',
       'ACTIVO'
WHERE NOT EXISTS (SELECT 1 FROM Usuario WHERE nombreUsuario = 'admin');

INSERT INTO Usuario
    (idRol, idCliente, nombreUsuario, correoElectronico, contrasenaHash, estado)
SELECT 2, 1, 'carlos', 'carlos.prueba@parksmart.com',
       'pbkdf2_sha256$310000$a98485dc8814d4282cb615cd6b301b76$40c8cc10c640859b687bfdd3d0a71dfff69f311e554610cc243293adae81a758',
       'ACTIVO'
WHERE NOT EXISTS (SELECT 1 FROM Usuario WHERE nombreUsuario = 'carlos');
