from datetime import datetime, timedelta
from os import getenv
import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
JWT_SECRET = getenv('JWT_SECRET', 'secret')
JWT_EXPIRES_IN = int(getenv('JWT_EXPIRES_IN', '3600'))


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=JWT_EXPIRES_IN)
    to_encode['exp'] = expire
    return jwt.encode(to_encode, JWT_SECRET, algorithm='HS256')


def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
