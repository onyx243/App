import os
import qrcode
import base64
from io import BytesIO


def generate_shop_qr(slug: str) -> str:
    url = f"{os.environ.get('BASE_URL')}/upload/{slug}"
    img = qrcode.make(url)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode()
