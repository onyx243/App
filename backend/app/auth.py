from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import os

from .main import db
from .models import UserModel, PyObjectId

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SignupBody(BaseModel):
    email: EmailStr
    password: str

class LoginBody(SignupBody):
    pass

def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(seconds=int(os.getenv("JWT_EXPIRES_IN", "3600")))
    to_encode = {**data, "exp": expire}
    return jwt.encode(to_encode, os.getenv("JWT_SECRET"), algorithm="HS256")

async def get_user(email: str):
    return await db.users.find_one({"email": email})

@router.post("/signup")
async def signup(body: SignupBody):
    if await get_user(body.email):
        raise HTTPException(status_code=400, detail="Email exists")
    hashed = pwd_context.hash(body.password)
    user = UserModel(email=body.email, password=hashed)
    res = await db.users.insert_one(user.dict(by_alias=True))
    user.id = res.inserted_id
    token = create_token({"id": str(user.id), "role": user.role})
    return {"token": token, "user": user}

@router.post("/login")
async def login(body: LoginBody):
    user = await get_user(body.email)
    if not user or not pwd_context.verify(body.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"id": str(user["_id"]), "role": user.get("role", "user")})
    return {"token": token, "user": UserModel(**user)}

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def auth_required(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, os.getenv("JWT_SECRET"), algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload
