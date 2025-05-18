import os
from datetime import datetime, timedelta
from typing import List, Optional

import boto3
import qrcode
from bson import ObjectId
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRES_IN = int(os.getenv("JWT_EXPIRES_IN", "3600"))
REFRESH_SECRET = os.getenv("REFRESH_SECRET")
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
USE_S3 = os.getenv("USE_S3", "false") == "true"
S3_BUCKET = os.getenv("S3_BUCKET")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncIOMotorClient(MONGO_URI)
db = client.get_default_database()

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

async def create_tokens(data: dict) -> Token:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=JWT_EXPIRES_IN)
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")
    refresh_token = jwt.encode({"sub": data["id"]}, REFRESH_SECRET, algorithm="HS256")
    return Token(access_token=access_token, refresh_token=refresh_token)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = await db.users.find_one({"_id": ObjectId(payload["id"] )})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        user["id"] = str(user["_id"])
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/auth/signup", response_model=Token)
async def signup(email: EmailStr, password: str):
    if await db.users.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email exists")
    hashed = pwd_context.hash(password)
    res = await db.users.insert_one({"email": email, "password": hashed, "role": "user"})
    return await create_tokens({"id": str(res.inserted_id), "role": "user"})

@app.post("/api/auth/login", response_model=Token)
async def login(email: EmailStr, password: str):
    user = await db.users.find_one({"email": email})
    if not user or not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return await create_tokens({"id": str(user["_id"]), "role": user["role"]})

@app.post("/api/auth/refresh", response_model=Token)
async def refresh(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=["HS256"])
        user = await db.users.find_one({"_id": ObjectId(payload["sub"])})
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return await create_tokens({"id": str(user["_id"]), "role": user["role"]})

@app.post("/api/upload/{slug}")
async def upload(slug: str, files: List[UploadFile] = File(...), user=Depends(get_current_user)):
    shop = await db.shops.find_one({"slug": slug})
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    paths = []
    for f in files:
        fname = f"{datetime.utcnow().timestamp()}-{f.filename}"
        if USE_S3:
            s3 = boto3.client("s3")
            s3.upload_fileobj(f.file, S3_BUCKET, fname)
            url = f"https://{S3_BUCKET}.s3.amazonaws.com/{fname}"
        else:
            dest = os.path.join(UPLOAD_DIR, fname)
            with open(dest, "wb") as out:
                out.write(await f.read())
            url = f"/uploads/{fname}"
        paths.append(url)
    await db.uploads.insert_one({
        "shop": shop["_id"],
        "user": ObjectId(user["id"]),
        "files": paths,
        "createdAt": datetime.utcnow(),
    })
    return {"files": paths}

@app.get("/api/dashboard")
async def dashboard(user=Depends(get_current_user)):
    uploads = db.uploads.find({"shop": user.get("shop"), "printed": {"$ne": True}}).sort("createdAt", -1)
    items = []
    async for u in uploads:
        u["id"] = str(u["_id"])
        items.append(u)
    return {"uploads": items}

@app.get("/api/download/{file_path:path}")
async def download(file_path: str):
    full = os.path.join(UPLOAD_DIR, file_path)
    if os.path.exists(full):
        return FileResponse(full)
    raise HTTPException(status_code=404, detail="File not found")


@app.get("/api/shops/{slug}/qr")
async def shop_qr(slug: str):
    img = qrcode.make(f"{os.getenv('BASE_URL')}/upload/{slug}")
    path = os.path.join(UPLOAD_DIR, f"{slug}.png")
    img.save(path)
    return FileResponse(path)
