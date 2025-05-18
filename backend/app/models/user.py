from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId

class UserIn(BaseModel):
    email: EmailStr
    password: str

class UserDB(UserIn):
    id: Optional[str] = Field(alias="_id")
    role: str = "user"
    shop: Optional[str] = None

class UserOut(BaseModel):
    id: str = Field(alias="_id")
    email: EmailStr
    role: str
    shop: Optional[str] = None
