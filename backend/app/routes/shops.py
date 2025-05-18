from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from ..db import db
from ..auth import role_required
from ..utils.qrcode import generate_shop_qr

router = APIRouter()


@router.post('/', dependencies=[Depends(role_required(['admin']))])
async def create_shop(data: dict):
    owner_id = data.get('ownerId')
    if not owner_id:
        raise HTTPException(status_code=400, detail='ownerId required')
    owner = await db.users.find_one({'_id': ObjectId(owner_id)})
    if not owner:
        raise HTTPException(status_code=400, detail='Owner not found')
    shop = {'name': data['name'], 'slug': data['slug'], 'owner': owner['_id']}
    res = await db.shops.insert_one(shop)
    await db.users.update_one({'_id': owner['_id']}, {'$set': {'shop': res.inserted_id, 'role': 'shopOwner'}})
    qr = generate_shop_qr(shop['slug'])
    shop['id'] = str(res.inserted_id)
    return {'shop': shop, 'qr': qr}


@router.get('/{slug}/qr')
async def get_qr(slug: str):
    shop = await db.shops.find_one({'slug': slug})
    if not shop:
        raise HTTPException(status_code=404, detail='Not found')
    qr = generate_shop_qr(shop['slug'])
    return {'qr': qr}
