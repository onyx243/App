from os import getenv, remove
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
from pymongo.collection import Collection
from ..deps import get_db, get_current_user
from ..utils.email import send_upload_email
import aiofiles
from uuid import uuid4
import boto3

router = APIRouter(prefix='/upload')

USE_S3 = getenv('USE_S3', 'false').lower() == 'true'
S3_BUCKET = getenv('S3_BUCKET')

s3 = boto3.client('s3') if USE_S3 else None

ALLOWED_MIME = {'image/png', 'image/jpeg', 'application/pdf'}
MAX_SIZE = 150 * 1024 * 1024
MAX_FILES = 12

async def save_file_local(file: UploadFile) -> str:
    path = f"uploads/{uuid4()}-{file.filename}"
    async with aiofiles.open(path, 'wb') as out:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            await out.write(chunk)
    return path

async def save_file_s3(file: UploadFile) -> str:
    key = f"{uuid4()}-{file.filename}"
    data = await file.read()
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=data)
    return f"https://{S3_BUCKET}.s3.amazonaws.com/{key}"

@router.post('/{slug}')
async def upload(slug: str, files: List[UploadFile] = File(...), db: Collection = Depends(get_db), user=Depends(get_current_user)):
    if len(files) > MAX_FILES:
        raise HTTPException(status_code=400, detail='Too many files')
    shop = await db.shops.find_one({'slug': slug})
    if not shop:
        raise HTTPException(status_code=404, detail='Shop not found')
    file_paths = []
    for f in files:
        if f.content_type not in ALLOWED_MIME:
            raise HTTPException(status_code=400, detail='Invalid file type')
        if f.size and f.size > MAX_SIZE:
            raise HTTPException(status_code=400, detail='File too large')
        if USE_S3:
            file_path = await save_file_s3(f)
        else:
            file_path = await save_file_local(f)
        file_paths.append(file_path)
    upload_doc = {
        'shop': shop['_id'],
        'user': user['_id'],
        'files': file_paths,
        'printed': False,
    }
    res = await db.uploads.insert_one(upload_doc)
    upload_doc['_id'] = res.inserted_id
    if shop.get('owner'):
        owner = await db.users.find_one({'_id': shop['owner']})
        if owner:
            await send_upload_email(owner['email'], file_paths)
    return {'upload': upload_doc}
