# Migración de proveedores

El archivo `database/migrations/02_proveedores.sql` agrega el rol PROVEEDOR, la entidad Proveedor y coordenadas reales para sectores/espacios.

Para una instalación limpia, `docker compose down -v` y luego `docker compose up --build` ejecutan el dump inicial y la migración. La migración se monta después del dump.

En una base existente, ejecutar el SQL una sola vez después de respaldar la base. Si alguna columna ya existe, omitir esa sentencia ALTER concreta.
