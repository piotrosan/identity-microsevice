from typing import List
from fastapi_mail import FastMail, MessageSchema, MessageType
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
