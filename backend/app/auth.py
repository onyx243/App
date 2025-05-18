import os
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
SECRET = os.getenv('JWT_SECRET', 'secret')
EXPIRE = int(os.getenv('JWT_EXPIRE', '3600'))


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=EXPIRE)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm="HS256")


def decode_token(token: str):
    return jwt.decode(token, SECRET, algorithms=["HS256"])


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )
    try:
        payload = decode_token(token)
        return payload
    except JWTError:
        raise credentials_exception


def role_required(roles):
    async def wrapper(user=Depends(get_current_user)):
        if user.get('role') not in roles:
            raise HTTPException(status_code=403, detail='Forbidden')
        return user
    return wrapper
