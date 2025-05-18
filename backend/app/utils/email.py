import smtplib
from email.message import EmailMessage
from os import getenv

async def send_upload_email(to: str, files: list[str]):
    user = getenv('EMAIL_USER')
    password = getenv('EMAIL_PASS')
    if not user or not password:
        return
    msg = EmailMessage()
    msg['Subject'] = 'New Print Upload'
    msg['From'] = user
    msg['To'] = to
    msg.set_content('Files uploaded: ' + ', '.join(files))
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(user, password)
            smtp.send_message(msg)
    except Exception as exc:
        print('Email send failed', exc)
