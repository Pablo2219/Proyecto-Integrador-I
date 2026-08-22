# Privacidad y Ley 8968

ParkSmart incorpora controles técnicos alineados con la Ley 8968 de Costa Rica y su Reglamento, pero este documento no sustituye una revisión jurídica profesional.

## Medidas incorporadas
- Registro separado por finalidad: cliente y proveedor.
- Consentimiento informado obligatorio (`aceptaPrivacidad`) antes de crear una cuenta.
- Contraseñas almacenadas mediante hash; nunca se guarda la contraseña en texto plano.
- Tokens de sesión firmados y con expiración.
- Endpoints de proveedor protegidos por rol y asociación del proveedor autenticado.
- Las reservas del proveedor se filtran únicamente a sus propios sectores/espacios.
- El mapa público expone únicamente datos comerciales necesarios para localizar el servicio; no publica datos personales del cliente.
- `.env` no debe contener secretos reales dentro de Git.
- Se conserva una bitácora de operaciones para trazabilidad.

## Derechos y operación
La Ley 8968 protege la autodeterminación informativa y establece reglas para el tratamiento de datos personales. El sistema debe ofrecer mecanismos reales para acceso, rectificación y supresión cuando correspondan, además de información clara sobre finalidades, responsables, destinatarios y medios de contacto.

Antes de pasar a producción se recomienda definir formalmente: responsable de la base, encargado(s), política de conservación, procedimiento de atención de derechos ARCO, gestión de incidentes, contratos con terceros y si alguna base requiere inscripción ante PRODHAB según el caso concreto.
