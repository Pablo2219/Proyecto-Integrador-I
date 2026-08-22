from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3307/parksmart"
    SECRET_KEY: str = "parksmart-cambie-esta-clave-en-produccion-2026"
    ACCESS_TOKEN_MINUTES: int = 480
    RESET_TOKEN_MINUTES: int = 15
    AUTH_DEBUG_RESET_TOKEN: bool = True

    # Cuenta administrativa para el entorno académico. Cambiar fuera de desarrollo.
    ADMIN_USERNAME: str = "admin"
    ADMIN_EMAIL: str = "admin@parksmart.com"
    ADMIN_PASSWORD: str = "Admin123*"
    ADMIN_RESET_PASSWORD_ON_STARTUP: bool = True

    NOTIFICATION_MODE: str = "SIMULATION"
    DEFAULT_PHONE_COUNTRY_CODE: str = "+506"

    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""
    SMTP_USE_TLS: bool = True

    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_SMS_FROM: str = ""
    TWILIO_WHATSAPP_FROM: str = ""

    FRONTEND_URL: str = "http://127.0.0.1:5500"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
