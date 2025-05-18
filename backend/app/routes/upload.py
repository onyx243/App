from typing import List
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from os import getenv
from pathlib import Path
import boto3
import time

from ..auth import get_current_user
from ..models import get_database
from ..utils.email import send_upload_email
from ..socket import sio

router = APIRouter(prefix="/api/upload")

db = get_database()
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)

USE_S3 = getenv("USE_S3", "false") == "true"


@router.post("/{slug}")
async def upload_files(slug: str, files: List[UploadFile] = File(...), current_user=Depends(get_current_user)):
    shop = await db.shops.find_one({"slug": slug})
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    file_paths = []
    if USE_S3:
        s3 = boto3.client("s3")
        for f in files:
            key = f"{int(time.time())}-{f.filename}"
            s3.upload_fileobj(f.file, getenv("S3_BUCKET"), key)
            file_paths.append(f"s3://{getenv('S3_BUCKET')}/{key}")
    else:
        for f in files:
            dest = uploads_dir / f"{int(time.time())}-{f.filename}"
            content = await f.read()
            dest.write_bytes(content)
            file_paths.append(str(dest))
    upload_doc = {
        "shop": shop["_id"],
        "user": current_user["id"],
        "files": file_paths,
        "printed": False,
    }
    res = await db.uploads.insert_one(upload_doc)
    upload_doc["id"] = str(res.inserted_id)
    await send_upload_email(shop["owner"], file_paths)
    await sio.emit("new-upload", upload_doc, to=str(shop["owner"]))
    return {"upload": upload_doc}
