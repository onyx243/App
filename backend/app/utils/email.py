import os
import smtplib
from email.mime.text import MIMEText


async def send_upload_email(to: str, files: list[str]):
    msg = MIMEText("Files uploaded: " + ", ".join(files))
    msg['Subject'] = 'New Print Upload'
    msg['From'] = os.environ.get('EMAIL_USER')
    msg['To'] = to
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()
            s.login(os.environ.get('EMAIL_USER'), os.environ.get('EMAIL_PASS'))
            s.send_message(msg)
    except Exception as exc:
        print('Email error', exc)
