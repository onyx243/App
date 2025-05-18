from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        return ObjectId(str(v))

class UserModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    email: EmailStr
    password: str
    role: str = "user"
    shop: Optional[PyObjectId] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ShopModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    name: str
    slug: str
    owner: PyObjectId

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UploadModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    shop: PyObjectId
    user: PyObjectId
    files: List[str]
    printed: bool = False

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
