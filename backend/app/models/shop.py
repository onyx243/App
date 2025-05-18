from typing import Optional
from pydantic import BaseModel, Field

class ShopIn(BaseModel):
    name: str

class ShopDB(ShopIn):
    id: Optional[str] = Field(alias="_id")
    slug: str
    owner: str

class ShopOut(BaseModel):
    id: str = Field(alias="_id")
    name: str
    slug: str
    owner: str
