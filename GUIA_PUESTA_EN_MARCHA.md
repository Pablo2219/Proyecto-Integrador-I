# Guía paso a paso

## 1. Requisitos
- Docker Desktop funcionando.
- Python 3.11+ para levantar únicamente el servidor estático del frontend.
- Navegador moderno con geolocalización habilitada.

## 2. Configurar `.env`
En PowerShell:
```powershell
Copy-Item .env.example .env
notepad .env
```
En desarrollo local podés dejar `MYSQL_ROOT_PASSWORD=root`, pero cambia `SECRET_KEY`. Si usás un MySQL externo, ajustá `DATABASE_URL`.

## 3. Arranque limpio
```powershell
docker compose down -v
docker compose up --build
```
Esperá a que `parksmart_db` esté `healthy` y `parksmart_api` esté arriba.

## 4. Frontend
En otra terminal, desde la raíz:
```powershell
python -m http.server 5500 --directory frontend
```
Abrí `http://127.0.0.1:5500`.

## 5. Probar registro
Pulsa **Crear una cuenta**. Elegí Cliente o Proveedor. El proveedor debe indicar nombre comercial. El checkbox de privacidad es obligatorio.

## 6. Probar proveedor
Iniciá sesión con la cuenta recién creada. En el panel proveedor:
- `+ Sector` → tocá una posición del mapa → nombre/precio → guardar.
- `+ Espacio` → tocá una posición → seleccioná sector/código/tipo → guardar.
- `Mis reservas` muestra solo reservas realizadas sobre espacios del proveedor autenticado.

## 7. Probar cliente
Registrá otra cuenta como cliente, agregá su vehículo desde el flujo existente y reservá un espacio. El proveedor verá esa reserva únicamente si pertenece a uno de sus espacios.

## 8. Swagger
`http://127.0.0.1:8000/docs`. El endpoint público de registro es `POST /auth/registro`; mapa público `GET /proveedores/mapa`; creación de sector/espacio y reservas de proveedor requieren JWT de proveedor.

## 9. Problemas frecuentes
- **Access denied MySQL:** verificá `MYSQL_ROOT_PASSWORD` y, si cambiaste credenciales después de crear el volumen, ejecutá `docker compose down -v` solo en desarrollo.
- **Puerto 3307 ocupado:** cambiá el puerto externo de `3307:3306` y `DATABASE_URL` si ejecutás API fuera de Docker.
- **Mapa vacío:** primero registrá un proveedor y publica un sector/espacio; Leaflet necesita internet para los tiles.
- **Cambios de tablas no aparecen:** recreá el volumen en desarrollo para ejecutar la migración inicial.
