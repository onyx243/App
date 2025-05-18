from fastapi import APIRouter, Depends
from bson import ObjectId
from ..db import db
from ..auth import role_required, get_current_user

router = APIRouter()


@router.get('/', dependencies=[Depends(role_required(['shopOwner']))])
async def list_uploads(user=Depends(get_current_user)):
    uploads = []
    async for u in db.uploads.find({'shop': ObjectId(user['shop']), 'printed': False}).sort('createdAt', -1):
        u['id'] = str(u['_id'])
        u.pop('_id', None)
        uploads.append(u)
    return {'uploads': uploads}


@router.patch('/{uid}/printed', dependencies=[Depends(role_required(['shopOwner']))])
async def mark_printed(uid: str):
    await db.uploads.update_one({'_id': ObjectId(uid)}, {'$set': {'printed': True}})
    return {'status': 'ok'}


@router.delete('/{uid}', dependencies=[Depends(role_required(['shopOwner']))])
async def delete_upload(uid: str):
    await db.uploads.delete_one({'_id': ObjectId(uid)})
    return {'status': 'ok'}
