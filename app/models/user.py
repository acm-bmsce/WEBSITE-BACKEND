from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(Document):
    username: str = Indexed(unique=True)
    email: EmailStr = Indexed(unique=True)
    hashed_password: str
    role: str = "coordinator"
    is_approved: bool = False
    
    # 🟢 NEW: Tracks if they forgot their password
    reset_requested: bool = False 

    class Settings:
        name = "users"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# 🟢 NEW: Schema for Admin to reset the password
class AdminResetPassword(BaseModel):
    user_id: str
    new_password: str