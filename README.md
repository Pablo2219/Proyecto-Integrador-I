# ParkSmart · Integrador II

Aplicación FastAPI + MySQL con frontend web adaptable para consultar parqueos, reservar, generar QR, administrar cuentas y operar proveedores.

## Cambios de esta versión
- Inicio de sesión real: se eliminó el flujo funcional de modo demostración. La cuenta administrativa existente continúa funcionando.
- Registro público de cuentas: únicamente `CLIENTE` o `PROVEEDOR`.
- Proveedores con sectores y espacios propios.
- Mapa Leaflet interactivo: el proveedor toca el mapa y se guardan latitud/longitud reales.
- Precio por hora por sector.
- Reservas separadas por rol: el cliente ve sus reservas; el proveedor ve reservas de sus propios espacios.
- Contraseñas con hash, JWT con expiración y validación de rol en backend.
- Consentimiento de privacidad registrado al crear cuenta.

## Puesta en marcha con Docker
1. Instalar Docker Desktop.
2. Copiar `.env.example` como `.env`.
3. Cambiar `SECRET_KEY` por una clave aleatoria larga. No subir `.env` a Git.
4. Para una instalación limpia: `docker compose down -v`.
5. Ejecutar `docker compose up --build`.
6. En otra terminal: `python -m http.server 5500 --directory frontend`.
7. Abrir `http://127.0.0.1:5500` y Swagger en `http://127.0.0.1:8000/docs`.

## Cuentas
La cuenta `admin` existente se mantiene y debe usarse para administración. Ya no existe un botón operativo de demo. Los clientes y proveedores nuevos se crean desde **Crear una cuenta**.

## Proveedor
Después de registrarse como proveedor, abrir **Panel proveedor**. Elegir `+ Sector` o `+ Espacio`, tocar el mapa, completar el formulario y guardar. El backend verifica que el sector pertenezca al proveedor autenticado.

## Importante con Docker
Las migraciones de `database/migrations` se ejecutan únicamente cuando MySQL inicializa un volumen nuevo. Por eso, después de cambiar el esquema, en desarrollo se recomienda `docker compose down -v` y `docker compose up --build`. En una base con datos reales, hacer respaldo y ejecutar la migración controladamente.

## Privacidad / Ley 8968
Se agregó consentimiento informado electrónico, registro de la versión del aviso, minimización de datos expuestos en el mapa y control de acceso por rol. La implementación técnica no sustituye asesoría jurídica ni la definición del responsable de la base, conservación, atención de derechos y obligaciones aplicables ante PRODHAB.
