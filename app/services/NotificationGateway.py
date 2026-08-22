import base64
import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from urllib import error, parse, request

from app.config.Settings import settings


@dataclass
class DeliveryResult:
    success: bool
    detail: str


class NotificationGateway:
    def send(self, canal: str, destinatario: str, titulo: str, mensaje: str) -> DeliveryResult:
        canal = canal.upper()
        if settings.NOTIFICATION_MODE.upper() != "REAL":
            return DeliveryResult(
                True,
                f"Envío simulado por {canal} hacia {destinatario}.",
            )

        if canal == "EMAIL":
            return self._send_email(destinatario, titulo, mensaje)
        if canal == "SMS":
            return self._send_twilio(destinatario, mensaje, whatsapp=False)
        if canal == "WHATSAPP":
            return self._send_twilio(destinatario, mensaje, whatsapp=True)
        if canal == "PUSH":
            return DeliveryResult(True, "Notificación push registrada para entrega interna.")
        return DeliveryResult(False, "Canal de notificación no soportado.")

    def _send_email(self, destinatario: str, titulo: str, mensaje: str) -> DeliveryResult:
        if not all([settings.SMTP_HOST, settings.SMTP_USERNAME, settings.SMTP_PASSWORD, settings.SMTP_FROM]):
            return DeliveryResult(False, "Faltan credenciales SMTP en el archivo .env.")
        email = EmailMessage()
        email["From"] = settings.SMTP_FROM
        email["To"] = destinatario
        email["Subject"] = titulo
        email.set_content(mensaje)
        try:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=15) as smtp:
                if settings.SMTP_USE_TLS:
                    smtp.starttls()
                smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                smtp.send_message(email)
            return DeliveryResult(True, "Correo enviado mediante SMTP.")
        except Exception as exc:
            return DeliveryResult(False, f"Error SMTP: {exc}")

    def _send_twilio(self, destinatario: str, mensaje: str, whatsapp: bool) -> DeliveryResult:
        if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
            return DeliveryResult(False, "Faltan credenciales de Twilio en el archivo .env.")
        origen = settings.TWILIO_WHATSAPP_FROM if whatsapp else settings.TWILIO_SMS_FROM
        if not origen:
            return DeliveryResult(False, "Falta configurar el número de origen de Twilio.")

        to_value = destinatario
        from_value = origen
        if whatsapp:
            if not to_value.startswith("whatsapp:"):
                to_value = f"whatsapp:{to_value}"
            if not from_value.startswith("whatsapp:"):
                from_value = f"whatsapp:{from_value}"

        body = parse.urlencode({"To": to_value, "From": from_value, "Body": mensaje}).encode()
        endpoint = (
            "https://api.twilio.com/2010-04-01/Accounts/"
            f"{settings.TWILIO_ACCOUNT_SID}/Messages.json"
        )
        req = request.Request(endpoint, data=body, method="POST")
        credentials = base64.b64encode(
            f"{settings.TWILIO_ACCOUNT_SID}:{settings.TWILIO_AUTH_TOKEN}".encode()
        ).decode()
        req.add_header("Authorization", f"Basic {credentials}")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        try:
            with request.urlopen(req, timeout=15) as response:
                if 200 <= response.status < 300:
                    return DeliveryResult(True, "Mensaje aceptado por Twilio.")
                return DeliveryResult(False, f"Twilio respondió con estado {response.status}.")
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")[:220]
            return DeliveryResult(False, f"Error Twilio {exc.code}: {detail}")
        except Exception as exc:
            return DeliveryResult(False, f"Error Twilio: {exc}")
