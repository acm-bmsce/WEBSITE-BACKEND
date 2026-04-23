from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# 1. Database Model
class Registration(Document):
    event_id: PydanticObjectId
    name: str
    email: EmailStr
    phone: str
    usn: str
    department: str
    is_team_event: bool = False
    team_name: Optional[str] = None
    # ✅ FIX: Use default_factory so it calculates the time AT the moment of registration
    registered_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "registrations"
        
        # ✅ Recommended: Add an index so you can quickly pull all registrations for a specific event
        indexes = [
            "event_id",
            [("event_id", 1), ("email", 1)] # Compound index to help prevent duplicate signups
        ]

# 2. Input Schema (What React sends)
class RegistrationCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    usn: str
    department: str
    is_team_event: bool = False
    team_name: Optional[str] = None