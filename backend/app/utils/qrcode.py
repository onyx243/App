from io import BytesIO
import qrcode

async def generate_shop_qr(slug: str) -> bytes:
    img = qrcode.make(f"https://printshop.example.com/upload/{slug}")
    buf = BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()
