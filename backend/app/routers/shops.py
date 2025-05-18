from fastapi import APIRouter, Depends, HTTPException
from slugify import slugify
from nanoid import generate
from pymongo.collection import Collection
from ..deps import get_db, get_current_user
from ..models.shop import ShopIn, ShopOut
from ..utils.qrcode import generate_shop_qr

router = APIRouter(prefix='/shops')

@router.post('/', response_model=ShopOut)
async def create_shop(payload: ShopIn, db: Collection = Depends(get_db), user=Depends(get_current_user)):
    if user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail='Forbidden')
    slug = slugify(payload.name) + '-' + generate(size=6)
    if await db.shops.find_one({'slug': slug}):
        raise HTTPException(status_code=400, detail='Slug exists')
    shop = {**payload.dict(), 'slug': slug, 'owner': user['_id']}
    res = await db.shops.insert_one(shop)
    shop['_id'] = res.inserted_id
    return shop

@router.get('/{slug}/qr')
async def get_qr(slug: str, db: Collection = Depends(get_db)):
    shop = await db.shops.find_one({'slug': slug})
    if not shop:
        raise HTTPException(status_code=404, detail='Not found')
    qr_bytes = await generate_shop_qr(slug)
    return {'qr': qr_bytes.decode('latin1')}
