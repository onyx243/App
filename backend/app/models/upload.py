from typing import List, Optional
from pydantic import BaseModel, Field

class UploadDB(BaseModel):
    id: Optional[str] = Field(alias="_id")
    shop: str
    user: str
    files: List[str]
    printed: bool = False

class UploadOut(BaseModel):
    id: str = Field(alias="_id")
    shop: str
    user: str
    files: List[str]
    printed: bool
