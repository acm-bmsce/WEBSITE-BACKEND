from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(Document):
    username: str = Indexed(unique=True) # Cannot have duplicate usernames
    email: EmailStr = Indexed(unique=True)
    hashed_password: str
    
    # Roles: "master" or "coordinator"
    role: str = "coordinator" 
    
    # Master is auto-approved; Coordinators start as False
    is_approved: bool = False 

    class Settings:
        name = "users"

# Schema for Registration Input
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str