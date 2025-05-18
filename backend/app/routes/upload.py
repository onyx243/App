import os
import time
import aiofiles
import boto3
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from bson import ObjectId
from ..db import db
from ..auth import get_current_user
from ..utils.email import send_upload_email
from ..main import sio

router = APIRouter()


def _public_path(path: str) -> str:
    return path


@router.post('/{slug}')
async def upload(slug: str, files: list[UploadFile] = File(...), user=Depends(get_current_user)):
    shop = await db.shops.find_one({'slug': slug})
    if not shop:
        raise HTTPException(status_code=404, detail='Shop not found')
    owner = await db.users.find_one({'_id': shop['owner']})
    file_paths = []
    if os.getenv('USE_S3') == 'true':
        s3 = boto3.client('s3')
        for file in files:
            key = f"{int(time.time())}-{file.filename}"
            s3.upload_fileobj(file.file, os.environ['S3_BUCKET'], key)
            file_paths.append(f"s3://{os.environ['S3_BUCKET']}/{key}")
    else:
        os.makedirs('uploads', exist_ok=True)
        for file in files:
            path = f"uploads/{int(time.time())}-{file.filename}"
            async with aiofiles.open(path, 'wb') as out:
                content = await file.read()
                await out.write(content)
            file_paths.append(path)
    upload_doc = {
        'shop': shop['_id'],
        'user': ObjectId(user['id']),
        'files': file_paths,
        'printed': False,
        'createdAt': int(time.time())
    }
    res = await db.uploads.insert_one(upload_doc)
    upload_doc['id'] = str(res.inserted_id)
    await send_upload_email(owner['email'], file_paths)
    await sio.emit('new-upload', upload_doc, to=str(owner['_id']))
    return {'upload': upload_doc}
