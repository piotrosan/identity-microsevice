import uuid
from typing import List
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from inrastructure.jwt.token import AccessToken
from inrastructure.settings.context_app import settings
from inrastructure.settings.mail import conf

from pydantic import EmailStr


async def send_mail(subject: str, body: str, recipients: List[EmailStr]):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=MessageType.html)
    fm = FastMail(conf)
    await fm.send_message(message)
