import os
import smtplib
from email.message import EmailMessage

async def send_upload_email(owner_id: str, files: list[str]):
    host = os.getenv('EMAIL_HOST')
    if not host:
        return
    msg = EmailMessage()
    msg['Subject'] = 'New Print Upload'
    msg['From'] = os.getenv('EMAIL_USER')
    msg['To'] = owner_id
    msg.set_content('Files uploaded:\n' + '\n'.join(files))
    try:
        with smtplib.SMTP(host, int(os.getenv('EMAIL_PORT', '25'))) as s:
            s.starttls()
            s.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
            s.send_message(msg)
    except Exception as exc:
        print('email error', exc)
