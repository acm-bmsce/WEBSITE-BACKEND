from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# 1. Database Model (Stored in MongoDB)
class Event(Document):
    title: str
    description: str
    date: datetime 
    image: Optional[str] = None 
    fullDescription: str
    outcomes: Optional[str] = None
    gallery: List[str] = [] 
    location: str
    attendees: int = 0
    registration_link: Optional[str] = None 
    
    # ✅ NEW: Marks event for the Carousel
    is_featured: bool = False 

    class Settings:
        name = "events"

    class Config:
        json_encoders = { datetime: lambda v: v.isoformat() }

# 2. Input Schema (Creating an Event)
class EventCreate(BaseModel):
    title: str
    description: str
    date_str: str = Field(..., description="DD-MM-YYYY")
    image: Optional[str] = None
    fullDescription: str
    outcomes: Optional[str] = None
    gallery: List[str] = []
    location: str
    attendees: str | int = 0
    registration_link: Optional[str] = None
    
    # ✅ NEW
    is_featured: bool = False

# 3. Update Schema (Editing an Event)
class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date_str: Optional[str] = None
    image: Optional[str] = None
    fullDescription: Optional[str] = None
    outcomes: Optional[str] = None
    gallery: Optional[List[str]] = None
    location: Optional[str] = None
    attendees: Optional[int] = None
    registration_link: Optional[str] = None
    
    # ✅ NEW
    is_featured: Optional[bool] = None

# 4. Response Schema (Sending to Frontend)
class EventResponse(BaseModel):
    id: PydanticObjectId = Field(alias="_id") # Maps Mongo's _id to id
    title: str
    description: str
    date: datetime
    image: Optional[str] = None
    fullDescription: str
    outcomes: Optional[str] = None
    gallery: List[str] = []
    location: str
    attendees: int = 0
    registration_link: Optional[str] = None
    
    # ✅ NEW
    is_featured: bool = False
    
    class Config:
        populate_by_name = True
        json_encoders = { datetime: lambda v: v.isoformat() }