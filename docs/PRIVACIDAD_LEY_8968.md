# Privacidad y Ley 8968

La Ley 8968 protege la autodeterminación informativa y regula datos personales en bases automatizadas o manuales. Su artículo 5 exige información previa, expresa y precisa sobre existencia de la base, finalidades, destinatarios, carácter obligatorio/facultativo, tratamiento, consecuencias y derechos; además, el consentimiento debe constar por escrito, incluso electrónicamente.

## Controles implementados
- El alta pública solo permite CLIENTE o PROVEEDOR.
- El registro exige `aceptaPrivacidad=true`.
- Se guarda versión del aviso, finalidad, fecha y usuario en `consentimiento_privacidad`.
- Las contraseñas se almacenan como hash y los tokens tienen expiración.
- El backend aplica autorización por rol para las funciones de proveedor.
- Un proveedor solo puede crear espacios en sectores que le pertenecen y solo ve reservas de esos espacios.
- El mapa público no expone teléfono, correo, identificación ni datos de clientes.
- El `.env` se mantiene fuera del repositorio.

## Pendientes antes de producción
Definir responsable de la base, canal para acceso/rectificación/supresión/revocación, política de conservación, gestión de incidentes, contratos con terceros y análisis de obligaciones ante PRODHAB. El Reglamento también exige medios simplificados para que los titulares ejerzan sus derechos.

Este documento es una implementación técnica/académica y no sustituye asesoría legal.
