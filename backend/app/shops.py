from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from .auth import auth_required
from .main import db
from .models import ShopModel, UserModel
from .utils.qrcode import generate_qr
from bson import ObjectId
import re

router = APIRouter()

class ShopBody(BaseModel):
    name: str
    slug: str
    owner_id: str

@router.post('/')
async def create_shop(body: ShopBody, user=Depends(auth_required)):
    if user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail='Forbidden')
    slug = re.sub(r'[^a-z0-9-]', '', body.slug.lower())
    shop = ShopModel(name=body.name, slug=slug, owner=ObjectId(body.owner_id))
    res = await db.shops.insert_one(shop.dict(by_alias=True))
    shop.id = res.inserted_id
    await db.users.update_one({'_id': ObjectId(body.owner_id)}, {'$set': {'role': 'shopOwner', 'shop': shop.id}})
    qr = generate_qr(slug)
    return {'shop': shop, 'qr': qr}

@router.get('/{slug}/qr')
async def qr(slug: str):
    shop = await db.shops.find_one({'slug': slug})
    if not shop:
        raise HTTPException(status_code=404, detail='Not found')
    return {'qr': generate_qr(slug)}
