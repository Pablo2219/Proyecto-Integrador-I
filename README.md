# ParkSmart · Integrador II

Aplicación FastAPI + MySQL con frontend web adaptable para consultar parqueos, reservar, generar QR, administrar cuentas y operar proveedores.

## Cambios de esta versión
- Inicio de sesión real: se eliminó el flujo funcional de modo demostración.
- Registro público de cuentas: únicamente `CLIENTE` o `PROVEEDOR`.
- La API crea/repara automáticamente la cuenta administrativa de desarrollo al iniciar.
- Proveedores con sectores y espacios propios.
- Mapa Leaflet interactivo: el proveedor toca el mapa y se guardan latitud/longitud reales.
- Precio por hora por sector.
- Reservas separadas por rol: el cliente ve sus reservas; el proveedor ve reservas de sus propios espacios.
- Contraseñas con PBKDF2, JWT con expiración y validación de rol en backend.
- Consentimiento de privacidad registrado al crear cuenta.
- CORS configurado para el frontend servido por `localhost`, `127.0.0.1` y redes privadas habituales.

## Puesta en marcha con Docker
1. Instalar Docker Desktop y tenerlo iniciado.
2. Copiar `.env.example` como `.env`.
3. Mantener estos valores de desarrollo si no necesitas cambiarlos:
   - `MYSQL_ROOT_PASSWORD=root`
   - `ADMIN_USERNAME=admin`
   - `ADMIN_EMAIL=admin@parksmart.com`
   - `ADMIN_PASSWORD=Admin123*`
   - `ADMIN_RESET_PASSWORD_ON_STARTUP=true`
4. Ejecutar `docker compose up --build -d`.
5. Verificar la API en `http://127.0.0.1:8000/`.
6. Verificar Swagger en `http://127.0.0.1:8000/docs`.
7. En otra terminal ejecutar `python -m http.server 5500 --directory frontend`.
8. Abrir `http://127.0.0.1:5500`.

## Cuenta administrativa de desarrollo
- Usuario: `admin`
- Correo: `admin@parksmart.com`
- Contraseña: `Admin123*`

La API comprueba al iniciar que los roles `ADMINISTRADOR`, `CLIENTE` y `PROVEEDOR` existan y que las columnas/tablas necesarias para proveedores y privacidad estén disponibles. Si ya existe una cuenta `admin`, se activa y, cuando `ADMIN_RESET_PASSWORD_ON_STARTUP=true`, se sincroniza con la contraseña indicada en `.env`.

**Importante:** esas credenciales son únicamente para desarrollo/académico. En producción deben cambiarse y `ADMIN_RESET_PASSWORD_ON_STARTUP` debe desactivarse.

## Qué hacer si ya tenías Docker ejecutándose
Primero:
```powershell
git pull origin main
docker compose up --build -d
docker logs parksmart_api
```

La API intentará reparar automáticamente un volumen existente. Solo es necesario `docker compose down -v` cuando quieras una base de datos completamente limpia y puedas perder los datos locales.

## Crear cuentas
En la pantalla de inicio de sesión aparece **Crear una cuenta**. Los únicos roles públicos son:
- `CLIENTE`
- `PROVEEDOR`

El administrador no puede ser creado desde el registro público.

## Proveedor
Después de registrarse como proveedor, el usuario obtiene las opciones de operación para crear sectores y espacios. En el mapa puede seleccionar una ubicación y guardar sus coordenadas reales. El backend comprueba que un proveedor solamente gestione sus propios sectores, espacios y reservas.

## Reservas
- Cliente: consulta y gestiona sus propias reservas.
- Proveedor: consulta únicamente reservas de sus sectores/espacios.
- Administrador: administra la operación general.

## Privacidad / Ley 8968
Se agregó consentimiento informado electrónico, registro de versión y finalidad, minimización de datos expuestos y control de acceso por rol. La implementación técnica no sustituye asesoría jurídica ni la definición del responsable de la base, conservación, atención de derechos y obligaciones aplicables ante PRODHAB.

## Diagnóstico rápido
Si la API no responde:
```powershell
docker ps
docker logs parksmart_db
docker logs parksmart_api
```

Si la API responde pero la cuenta no permite entrar:
```powershell
curl http://127.0.0.1:8000/
```

La respuesta correcta debe indicar la versión `2.2.0` y `estado: base de datos verificada`.
