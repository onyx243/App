from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from ..auth import get_current_user, require_roles
from ..models import get_database

router = APIRouter(prefix="/api/dashboard")

db = get_database()


@router.get("/")
@require_roles(["shopOwner"])
async def list_uploads(current_user=Depends(get_current_user)):
    cursor = db.uploads.find({"shop": current_user.get("shop"), "printed": False}).sort("_id", -1)
    uploads = []
    async for u in cursor:
        u["id"] = str(u["_id"])
        uploads.append(u)
    return {"uploads": uploads}


@router.patch("/{upload_id}/printed")
@require_roles(["shopOwner"])
async def mark_printed(upload_id: str, current_user=Depends(get_current_user)):
    result = await db.uploads.find_one_and_update({"_id": ObjectId(upload_id)}, {"$set": {"printed": True}}, return_document=True)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    result["id"] = str(result["_id"])
    return {"upload": result}


@router.delete("/{upload_id}")
@require_roles(["shopOwner"])
async def delete_upload(upload_id: str, current_user=Depends(get_current_user)):
    await db.uploads.delete_one({"_id": ObjectId(upload_id)})
    return {}
