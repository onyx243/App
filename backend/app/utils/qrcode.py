import qrcode
from io import BytesIO
import base64
from os import getenv

async def generate_shop_qr(slug: str) -> str:
    url = f"{getenv('BASE_URL', 'http://localhost:3000')}/upload/{slug}"
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode()
