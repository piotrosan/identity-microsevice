import os

from fastapi_mail import ConnectionConfig
from pydantic import SecretStr, EmailStr

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('mail_username'),
    MAIL_PASSWORD=SecretStr(os.getenv('mail_password')),
    MAIL_FROM=os.getenv('mail_from'),
    MAIL_PORT=587,
    MAIL_SERVER="whatsgoingon.home.pl",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)