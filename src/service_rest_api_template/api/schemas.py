from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    name: str
    items: List[Item] = []

    class Config:
        orm_mode = True

class Message(BaseModel):
    message: str

class HelloResponse(BaseModel):
    message: str
