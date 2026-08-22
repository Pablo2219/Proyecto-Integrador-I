# ParkSmart · Integrador II

Aplicación FastAPI + MySQL con interfaz web adaptable para consultar espacios, reservar, generar QR, administrar cuentas y enviar notificaciones multicanal.

## Funciones principales

- Interfaz móvil y de escritorio con tema claro/oscuro.
- Inicio de sesión con token firmado.
- Roles `ADMINISTRADOR` y `CLIENTE`.
- Recuperación, cambio de contraseña y cambio de cuenta.
- CRUD administrativo de usuarios.
- Notificaciones `EMAIL`, `SMS`, `WHATSAPP` y `PUSH` desde Swagger o la interfaz.
- Modo de simulación para revisar la aplicación sin consumir servicios externos.

## Inicio rápido

```powershell
Copy-Item .env.example .env
docker compose down -v
docker compose up --build
python -m http.server 5500 --directory frontend
```

- Interfaz: `http://127.0.0.1:5500`
- Swagger: `http://127.0.0.1:8000/docs`

Credenciales académicas:

- Administrador: `admin` / `Admin123*`
- Cliente: `carlos` / `Cliente123*`

La explicación completa se encuentra en [GUIA_IMPLEMENTACION_INTEGRADOR_II.md](GUIA_IMPLEMENTACION_INTEGRADOR_II.md).
