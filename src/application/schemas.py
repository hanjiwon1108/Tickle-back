from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    
    class Config:
        orm_mode = True

from src.domain.models import AssetType
from datetime import datetime

class AssetBase(BaseModel):
    type: AssetType
    name: str
    balance: float
    currency: str = "KRW"

class AssetCreate(AssetBase):
    pass

class AssetResponse(AssetBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str
    date: datetime = datetime.utcnow()

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True
