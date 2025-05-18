from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from .auth import auth_required
from .main import db
from .models import UploadModel

router = APIRouter()

@router.get('/')
async def pending(user=Depends(auth_required)):
    if user.get('role') != 'shopOwner':
        raise HTTPException(status_code=403, detail='Forbidden')
    uploads = []
    cursor = db.uploads.find({'shop': ObjectId(user.get('shop')), 'printed': False})
    async for doc in cursor:
        uploads.append(UploadModel(**doc))
    return {'uploads': uploads}

@router.patch('/{uid}/printed')
async def mark_printed(uid: str, user=Depends(auth_required)):
    if user.get('role') != 'shopOwner':
        raise HTTPException(status_code=403, detail='Forbidden')
    await db.uploads.update_one({'_id': ObjectId(uid)}, {'$set': {'printed': True}})
    return {'status': 'ok'}

@router.delete('/{uid}')
async def delete_upload(uid: str, user=Depends(auth_required)):
    if user.get('role') != 'shopOwner':
        raise HTTPException(status_code=403, detail='Forbidden')
    await db.uploads.delete_one({'_id': ObjectId(uid)})
    return {'status': 'ok'}
