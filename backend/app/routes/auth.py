from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from os import getenv

from ..models import get_database
from ..auth import create_access_token, hash_password, verify_password
from ..auth import init_auth

router = APIRouter(prefix="/api/auth")

db = get_database()


class UserIn(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
async def signup(data: UserIn):
    if await db.users.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="Email exists")
    user = {"email": data.email, "password": hash_password(data.password), "role": "user"}
    res = await db.users.insert_one(user)
    user["id"] = str(res.inserted_id)
    token = create_access_token({"id": user["id"], "role": user["role"]})
    return {"token": token, "user": {"id": user["id"], "email": user["email"], "role": user["role"]}}


@router.post("/login")
async def login(data: UserIn):
    user = await db.users.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_id = str(user["_id"])
    token = create_access_token({"id": user_id, "role": user.get("role", "user")})
    return {"token": token, "user": {"id": user_id, "email": user["email"], "role": user.get("role", "user")}}
