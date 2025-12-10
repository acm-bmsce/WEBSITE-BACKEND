from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Project(Document):
    # 1. OPTION 1: Map _id to id for the frontend
    id: Optional[PydanticObjectId] = Field(alias="_id", default=None)
    
    title: str
    description: str
    
    # Matching Frontend Field Names
    author: str  # Was 'team_members'
    githubUrl: Optional[str] = None # Was 'github_link'
    imageUrl: Optional[str] = None  # Was 'image_url'
    
    # New Fields required by your UI
    categories: List[str] = [] 
    techStack: List[str] = []
    
    # Internal logic fields
    status: str = "PENDING"
    submission_date: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "projects"
    
    class Config:
        populate_by_name = True
        json_encoders = { datetime: lambda v: v.isoformat() }

# Input Schema (What you send to create it)
class ProjectCreate(BaseModel):
    title: str
    description: str
    author: str
    githubUrl: Optional[str] = None
    imageUrl: Optional[str] = None
    categories: List[str] = []
    techStack: List[str] = []
    status: Optional[str] = "PENDING"