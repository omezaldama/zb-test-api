from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    role: Optional[str]

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    email: Optional[str]
    role: Optional[str]

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
