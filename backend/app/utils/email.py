import smtplib
from email.message import EmailMessage
from os import getenv

SMTP_HOST = getenv('SMTP_HOST')
SMTP_PORT = int(getenv('SMTP_PORT', '587'))
SMTP_USER = getenv('SMTP_USER')
SMTP_PASS = getenv('SMTP_PASS')
SMTP_TLS = getenv('SMTP_TLS', 'true').lower() == 'true'

async def send_upload_email(to_email: str, files: list[str]) -> None:
    msg = EmailMessage()
    msg['Subject'] = 'New upload received'
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg.set_content('\n'.join(files))
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        if SMTP_TLS:
            s.starttls()
        if SMTP_USER:
            s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)
