# Guía paso a paso

## 1. Requisitos
- Docker Desktop funcionando.
- Python 3.11+ para levantar el servidor estático del frontend.
- Navegador moderno con JavaScript y geolocalización.

## 2. Configurar `.env`
```powershell
Copy-Item .env.example .env
notepad .env
```
En desarrollo dejá `MYSQL_ROOT_PASSWORD=root` si no necesitás otra clave. **Cambiá `SECRET_KEY`** por una cadena aleatoria larga. El `.gitignore` ya evita subir `.env`.

## 3. Arranque limpio recomendado
La imagen oficial de MySQL ejecuta los `.sql` de `/docker-entrypoint-initdb.d` en orden al inicializar un volumen nuevo. citeturn2search0
```powershell
docker compose down -v
docker compose up --build
```
No cierres esa terminal. Esperá a que aparezcan los contenedores `parksmart_db` y `parksmart_api`.

## 4. Frontend
En otra PowerShell, desde la raíz:
```powershell
python -m http.server 5500 --directory frontend
```
Abrí `http://127.0.0.1:5500`.

## 5. Crear cliente o proveedor
En login aparece **Crear una cuenta**. Los roles públicos son únicamente Cliente y Proveedor. El consentimiento de privacidad es obligatorio.

## 6. Proveedor
Después de crear una cuenta de proveedor:
1. Entrá con sus credenciales.
2. Abrí **Panel proveedor**.
3. `+ Sector` → tocá el mapa → nombre + precio/hora → guardar.
4. `+ Espacio` → tocá el mapa → sector + código + tipo → guardar.
5. `Mis reservas` muestra las reservas de los espacios pertenecientes a ese proveedor.

Las coordenadas se almacenan en la base como latitud/longitud y el backend verifica la propiedad del sector antes de permitir agregar espacios.

## 7. Cliente
Creá una cuenta cliente, agregá su vehículo usando el flujo existente y reservá. El cliente consulta sus reservas; el proveedor solo consulta las reservas de sus propios espacios.

## 8. Swagger
- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Registro: `POST /auth/registro`
- Mapa: `GET /proveedores/mapa`
- Sectores: `POST /proveedores/sectores` (proveedor autenticado)
- Espacios: `POST /proveedores/espacios` (proveedor autenticado)
- Reservas proveedor: `GET /proveedores/reservas` (proveedor autenticado)

## 9. Si ya tenías una base creada
Los scripts de inicialización de MySQL no vuelven a ejecutarse sobre un volumen existente. En desarrollo académico, hacé respaldo si necesitás los datos y luego:
```powershell
docker compose down -v
docker compose up --build
```
En producción nunca borres el volumen: respaldá y ejecutá la migración de forma controlada.
