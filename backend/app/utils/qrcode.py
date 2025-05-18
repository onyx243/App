import qrcode
import base64
from io import BytesIO

BASE_URL = 'https://printshop.example.com/upload/'

def generate_qr(slug: str) -> str:
    qr = qrcode.QRCode(box_size=3, border=2)
    qr.add_data(BASE_URL + slug)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode()
