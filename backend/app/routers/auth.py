from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection
from ..deps import get_db
from ..models.user import UserIn, UserOut
from ..utils.auth_utils import hash_password, verify_password, create_token
from bson import ObjectId

router = APIRouter(prefix='/auth')

@router.post('/signup')
async def signup(payload: UserIn, db: Collection = Depends(get_db)):
    if await db.users.find_one({'email': payload.email}):
        raise HTTPException(status_code=400, detail='Email exists')
    user = payload.dict()
    user['password'] = hash_password(user['password'])
    user['role'] = 'user'
    res = await db.users.insert_one(user)
    user['_id'] = res.inserted_id
    token = create_token({'id': str(res.inserted_id), 'role': user['role']})
    return {'token': token, 'user': UserOut(**user)}

@router.post('/login')
async def login(payload: UserIn, db: Collection = Depends(get_db)):
    user = await db.users.find_one({'email': payload.email})
    if not user or not verify_password(payload.password, user['password']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_token({'id': str(user['_id']), 'role': user['role']})
    return {'token': token, 'user': UserOut(**user)}
