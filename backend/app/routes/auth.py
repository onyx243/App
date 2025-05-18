from fastapi import APIRouter, HTTPException
from ..db import db
from ..auth import create_token
from passlib.hash import bcrypt

router = APIRouter()


@router.post('/signup')
async def signup(data: dict):
    if await db.users.find_one({'email': data['email']}):
        raise HTTPException(status_code=400, detail='Email exists')
    data['password'] = bcrypt.hash(data['password'])
    data['role'] = data.get('role', 'user')
    res = await db.users.insert_one(data)
    data['id'] = str(res.inserted_id)
    token = create_token({'id': data['id'], 'role': data['role']})
    return {'token': token, 'user': data}


@router.post('/login')
async def login(data: dict):
    user = await db.users.find_one({'email': data['email']})
    if not user or not bcrypt.verify(data['password'], user['password']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    user['id'] = str(user['_id'])
    token = create_token({'id': user['id'], 'role': user['role']})
    user.pop('_id', None)
    return {'token': token, 'user': user}
