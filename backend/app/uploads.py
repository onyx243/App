from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import List
from bson import ObjectId
import os
import boto3

from .auth import auth_required
from .main import db
from .models import UploadModel
from .utils.email import send_upload_email

router = APIRouter()

UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post('/{slug}')
async def upload_files(slug: str, files: List[UploadFile] = File(...), user=Depends(auth_required)):
    shop = await db.shops.find_one({'slug': slug})
    if not shop:
        raise HTTPException(status_code=404, detail='Shop not found')

    paths = []
    for f in files:
        if os.getenv('USE_S3') == 'true':
            s3 = boto3.client('s3', region_name=os.getenv('S3_REGION'))
            key = f"{ObjectId()}-{f.filename}"
            s3.upload_fileobj(f.file, os.getenv('S3_BUCKET'), key)
            url = f"https://{os.getenv('S3_BUCKET')}.s3.amazonaws.com/{key}"
            paths.append(url)
        else:
            path = os.path.join(UPLOAD_DIR, f"{ObjectId()}-{f.filename}")
            with open(path, 'wb') as out:
                out.write(await f.read())
            paths.append(path)

    upload = UploadModel(shop=shop['_id'], user=ObjectId(user['id']), files=paths)
    res = await db.uploads.insert_one(upload.dict(by_alias=True))
    upload.id = res.inserted_id

    await send_upload_email(shop['owner'], paths)
    # socket.io notifications could be added here
    return {'upload': upload}
