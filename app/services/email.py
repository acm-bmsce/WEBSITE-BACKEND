# app/services/email.py

import aiosmtplib
from email.message import EmailMessage
import os

EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

async def send_email(to_email: str, event_name: str):
    msg = EmailMessage()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = "Registration Successful"

    msg.set_content(f"You registered for {event_name}")

    await aiosmtplib.send(
        msg,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username=EMAIL,
        password=PASSWORD,
    )