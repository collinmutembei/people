from pathlib import Path
from typing import Any, Dict, List

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import BaseModel, EmailStr

ACCOUNT_VERIFICATION_EMAIL_SUBJECT = "Account verification token"
PASSWORD_RESET_EMAIL_SUBJECT = "Password reset token"


class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]


conf = ConnectionConfig(
    MAIL_USERNAME="username",
    MAIL_PASSWORD="password",
    MAIL_FROM="admin@people.api",
    MAIL_PORT=1025,
    MAIL_SERVER="localhost",
    MAIL_TLS=False,
    MAIL_SSL=False,
    TEMPLATE_FOLDER=Path(__file__).parent / "templates",
)

fm = FastMail(conf)


async def sender(email: EmailSchema, subject: str, template_name: str):

    message = MessageSchema(
        subject=subject,
        recipients=email.dict().get("email"),
        template_body=email.dict().get("body"),
    )
    await fm.send_message(message, template_name=f"{template_name}.html")
