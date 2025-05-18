from os import remove
from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection
from ..deps import get_db, get_current_user

router = APIRouter(prefix='/dashboard')

@router.get('/')
async def list_uploads(db: Collection = Depends(get_db), user=Depends(get_current_user)):
    if user.get('role') != 'shopOwner':
        raise HTTPException(status_code=403, detail='Forbidden')
    uploads = await db.uploads.find({'shop': user.get('shop'), 'printed': False}).to_list(length=100)
    return {'uploads': uploads}

@router.patch('/{upload_id}/printed')
async def mark_printed(upload_id: str, db: Collection = Depends(get_db), user=Depends(get_current_user)):
    if user.get('role') != 'shopOwner':
        raise HTTPException(status_code=403, detail='Forbidden')
    upload = await db.uploads.find_one({'_id': upload_id})
    if not upload:
        raise HTTPException(status_code=404, detail='Not found')
    await db.uploads.update_one({'_id': upload_id}, {'$set': {'printed': True}})
    return {'status': 'ok'}

@router.delete('/{upload_id}')
async def delete_upload(upload_id: str, db: Collection = Depends(get_db), user=Depends(get_current_user)):
    if user.get('role') != 'shopOwner':
        raise HTTPException(status_code=403, detail='Forbidden')
    upload = await db.uploads.find_one({'_id': upload_id})
    if not upload:
        raise HTTPException(status_code=404, detail='Not found')
    await db.uploads.delete_one({'_id': upload_id})
    for f in upload['files']:
        try:
            remove(f)
        except FileNotFoundError:
            pass
    return {'status': 'deleted'}
