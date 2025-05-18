from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from ..auth import get_current_user, require_roles
from ..models import get_database
from ..utils.qrcode import generate_shop_qr

router = APIRouter(prefix="/api/shops")

db = get_database()


class ShopIn(BaseModel):
    name: str
    slug: str
    ownerId: str


@router.post("/")
@require_roles(["admin"])
async def create_shop(data: ShopIn, current_user=Depends(get_current_user)):
    if await db.shops.find_one({"slug": data.slug}):
        raise HTTPException(status_code=400, detail="Slug exists")
    shop = {"name": data.name, "slug": data.slug, "owner": data.ownerId}
    res = await db.shops.insert_one(shop)
    shop["id"] = str(res.inserted_id)
    await db.users.update_one({"_id": data.ownerId}, {"$set": {"shop": shop["id"], "role": "shopOwner"}})
    qr = await generate_shop_qr(data.slug)
    return {"shop": shop, "qr": qr}


@router.get("/{slug}/qr")
async def get_shop_qr(slug: str):
    shop = await db.shops.find_one({"slug": slug})
    if not shop:
        raise HTTPException(status_code=404, detail="Not found")
    qr = await generate_shop_qr(slug)
    return {"qr": qr}
