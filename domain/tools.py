import uuid
from typing import List
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from inrastructure.jwt.token import AccessToken
from inrastructure.settings.context_app import settings
from inrastructure.settings.mail import conf

from pydantic import EmailStr


def generate_activation_link(email: str):
    access_token = AccessToken(
        token_type="activation_token",
        user_identifier=uuid.uuid5(
            namespace=uuid.NAMESPACE_DNS, name=email
        )
    )
    link = f"{settings.base_link}/activate/{access_token.get_access_token()}"
    return link


async def send_mail(subject: str, body: str, recipients: List[EmailStr]):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=MessageType.html)
    fm = FastMail(conf)
    await fm.send_message(message)
