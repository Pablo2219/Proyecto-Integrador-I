# ParkSmart · Implementación del Proyecto Integrador II

## 1. Alcance implementado

Esta versión amplía el Proyecto Integrador I con cuatro grupos de mejoras:

1. **Interfaz visual renovada:** pantalla de acceso, formularios más nítidos, paneles con mejor jerarquía, colores consistentes, diseño adaptable a celular y computadora, tema claro/oscuro y panel administrativo.
2. **Notificaciones multicanal:** el `POST /notificaciones/` permite seleccionar `EMAIL`, `SMS`, `WHATSAPP` o `PUSH` desde Swagger o desde el panel administrativo.
3. **Usuarios y roles:** se incorporaron las entidades `Usuario` y `Rol`, autenticación con token firmado, usuarios `ADMINISTRADOR` y `CLIENTE`, y un CRUD administrativo de cuentas.
4. **Gestión de cuenta:** inicio de sesión, recuperación de contraseña, cambio de contraseña y cambio/cierre de cuenta.

## 2. Credenciales académicas iniciales

| Rol | Usuario | Contraseña | Cliente asociado |
|---|---|---|---|
| Administrador | `admin` | `Admin123*` | No aplica |
| Cliente | `carlos` | `Cliente123*` | Cliente ID `1` |

Estas credenciales se crean automáticamente al inicializar una base de datos nueva. Cambiarlas antes de utilizar el sistema fuera de un entorno académico.

## 3. Iniciar el proyecto

### 3.1 Preparar variables de entorno

En PowerShell, desde la carpeta del proyecto:

```powershell
Copy-Item .env.example .env
```

El modo predeterminado de notificaciones es `SIMULATION`. En este modo no se consumen servicios externos, pero el sistema registra el canal, el destinatario, el estado y la fecha de envío.

### 3.2 Crear nuevamente la base de datos

Esta es la opción más sencilla cuando no se necesitan conservar datos anteriores:

```powershell
docker compose down -v
docker compose up --build
```

La eliminación del volumen es necesaria si MySQL ya había ejecutado el archivo SQL antiguo, porque los scripts de inicialización solo se ejecutan al crear el volumen por primera vez.

### 3.3 Conservar una base de datos existente

Con los contenedores encendidos, ejecutar la migración:

```powershell
Get-Content .\database\migrations\002_integrador2_auth_notificaciones.sql |
    docker exec -i parksmart_db mysql -uroot -proot parksmart
```

Después reconstruir la API:

```powershell
docker compose up --build -d
```

### 3.4 Servir la interfaz

Con Live Server en Visual Studio Code, abrir `frontend/index.html`. Otra alternativa:

```powershell
python -m http.server 5500 --directory frontend
```

Direcciones principales:

- Aplicación: `http://127.0.0.1:5500`
- Swagger: `http://127.0.0.1:8000/docs`
- API: `http://127.0.0.1:8000`

## 4. Probar autenticación en Swagger

### Paso 1. Iniciar sesión

Usar `POST /auth/login`:

```json
{
  "usuario": "admin",
  "contrasena": "Admin123*"
}
```

La respuesta contiene `accessToken`, información del usuario, rol y tiempo de expiración.

### Paso 2. Autorizar Swagger

1. Presionar **Authorize** en la parte superior de Swagger.
2. Pegar únicamente el valor de `accessToken`.
3. Confirmar la autorización.

Los endpoints de `/usuarios` requieren el rol `ADMINISTRADOR`.

### Paso 3. Consultar la cuenta actual

Ejecutar `GET /auth/me`. Debe devolver el usuario conectado y su rol.

## 5. Crear administradores y clientes

Usar `POST /usuarios/` con una sesión de administrador.

### Usuario cliente

```json
{
  "nombreUsuario": "cliente02",
  "correoElectronico": "cliente02@parksmart.com",
  "contrasena": "Cliente123*",
  "rol": "CLIENTE",
  "idCliente": 1
}
```

Un usuario con rol `CLIENTE` debe relacionarse con un registro existente de la tabla `Cliente`.

### Usuario administrador

```json
{
  "nombreUsuario": "admin02",
  "correoElectronico": "admin02@parksmart.com",
  "contrasena": "Admin123*",
  "rol": "ADMINISTRADOR",
  "idCliente": null
}
```

También se pueden crear ambos tipos desde **Perfil → Administración** en la interfaz.

## 6. Notificaciones por Email, SMS, WhatsApp y Push

El endpoint principal es `POST /notificaciones/`. El campo `canal` acepta:

- `EMAIL`
- `SMS`
- `WHATSAPP`
- `PUSH`

Cuando `destinatario` se omite, ParkSmart utiliza automáticamente:

- El correo del cliente para `EMAIL`.
- El teléfono del cliente para `SMS` o `WHATSAPP`.
- El identificador interno del cliente para `PUSH`.

### Ejemplo SMS

```json
{
  "idCliente": 1,
  "idReserva": null,
  "idPago": null,
  "idDeuda": null,
  "tipoNotificacion": "SISTEMA",
  "canal": "SMS",
  "titulo": "Reserva próxima",
  "mensaje": "Tu reserva inicia dentro de 30 minutos.",
  "destinatario": "+50688889999",
  "observaciones": "Prueba desde Swagger",
  "enviarAhora": true
}
```

### Ejemplo WhatsApp

```json
{
  "idCliente": 1,
  "tipoNotificacion": "PAGO",
  "canal": "WHATSAPP",
  "titulo": "Pago confirmado",
  "mensaje": "Tu pago fue registrado correctamente en ParkSmart.",
  "destinatario": "+50688889999",
  "enviarAhora": true
}
```

### Estados posibles

- `PENDIENTE`: se creó, pero no se solicitó envío inmediato.
- `ENVIADA`: el proveedor aceptó el envío o se procesó correctamente en simulación.
- `FALLIDA`: ocurrió un error de configuración o comunicación.
- `LEIDA`: el cliente abrió o confirmó el aviso.
- `ANULADA`: la notificación fue cancelada.

## 7. Activar envíos reales

Cambiar en `.env`:

```env
NOTIFICATION_MODE=REAL
```

### Correo electrónico mediante SMTP

Configurar:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=correo@gmail.com
SMTP_PASSWORD=contrasena_de_aplicacion
SMTP_FROM=correo@gmail.com
SMTP_USE_TLS=true
```

Para Gmail se recomienda una contraseña de aplicación, no la contraseña normal de la cuenta.

### SMS y WhatsApp mediante Twilio

Configurar:

```env
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_SMS_FROM=+1XXXXXXXXXX
TWILIO_WHATSAPP_FROM=+1XXXXXXXXXX
```

La cuenta de Twilio debe tener habilitado el número de SMS y, para WhatsApp, el Sandbox o un remitente aprobado.

## 8. Recuperar y cambiar contraseña

### Desde la interfaz

- En la pantalla de acceso: **¿Olvidaste tu contraseña?**
- Dentro de la cuenta: **Perfil → Cambiar contraseña**
- Para usar otro usuario: **Perfil → Cambiar cuenta**

### Desde Swagger

- `POST /auth/solicitar-restablecimiento`
- `POST /auth/restablecer-contrasena`
- `PUT /auth/cambiar-contrasena`

En modo académico, `AUTH_DEBUG_RESET_TOKEN=true` devuelve temporalmente el token de recuperación en la respuesta para facilitar las pruebas. En producción debe cambiarse a `false`.

## 9. Archivos principales agregados

### Backend

- `app/controllers/AuthController.py`
- `app/controllers/UsuarioController.py`
- `app/services/AuthService.py`
- `app/services/UsuarioService.py`
- `app/services/NotificationGateway.py`
- `app/repositories/UsuarioRepository.py`
- `app/repositories/RolRepository.py`
- `app/models/Usuario.py`
- `app/models/Rol.py`
- `app/config/Security.py`

### Frontend

- `frontend/js/auth.js`
- Nuevas secciones y diálogos en `frontend/index.html`
- Nuevos estilos al final de `frontend/css/styles.css`

### Base de datos

- Usuarios iniciales en `database/parksmart_db.sql`
- Migración `database/migrations/002_integrador2_auth_notificaciones.sql`

## 10. Consideraciones de seguridad

- Cambiar `SECRET_KEY` y las contraseñas académicas.
- No subir el archivo `.env` al repositorio.
- Desactivar `AUTH_DEBUG_RESET_TOKEN` fuera de las demostraciones.
- Usar HTTPS al desplegar.
- Utilizar credenciales de Twilio y SMTP almacenadas como secretos del proveedor cloud.
- Mantener el endpoint de usuarios restringido a administradores.
