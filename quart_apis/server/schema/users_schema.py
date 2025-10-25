from pydantic import BaseModel,EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(UserCreate):
    id: str
    username: str
    createdAt: datetime
    updatedAt: datetime | None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None

class UserCustomRead(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: str
    createdAt: datetime
    updatedAt: datetime | None
    
    class Config:
        from_attributes = True
    