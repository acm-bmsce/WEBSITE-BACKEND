from beanie import Document
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

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
    
    # NEW FIELD: Stores the Google Form URL
    registration_link: Optional[str] = None 

    class Settings:
        name = "events"

    class Config:
        json_encoders = { datetime: lambda v: v.isoformat() }

# Update the Input Schema too
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
    registration_link: Optional[str] = None # <--- Add this here too

# NEW: Schema for UPDATING an event (All fields optional)
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