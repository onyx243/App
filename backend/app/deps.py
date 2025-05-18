from os import getenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
from .utils.auth_utils import decode_token

MONGO_URI = getenv('MONGODB_URI')
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_default_database()

security = HTTPBearer()

async def get_db() -> Collection:
    return db

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = decode_token(credentials.credentials)
    except Exception as exc:  # broad for brevity
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token') from exc
    user = await db.users.find_one({'_id': payload['id']})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user
