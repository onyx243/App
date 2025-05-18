from functools import lru_cache
from os import getenv

from motor.motor_asyncio import AsyncIOMotorClient


@lru_cache
def get_database():
    uri = getenv("MONGODB_URI", "mongodb://localhost:27017/printshop")
    client = AsyncIOMotorClient(uri)
    return client.get_default_database()
