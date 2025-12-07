from beanie import Document
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Project(Document):
    title: str
    description: str
    team_members: List[str] # List of names e.g. ["Alice", "Bob"]
    
    # "PENDING" (default), "APPROVED", or "REJECTED"
    status: str = "PENDING" 
    
    submission_date: datetime = Field(default_factory=datetime.now)
    
    # Optional links (GitHub, Demo Video, etc.)
    github_link: Optional[str] = None
    demo_link: Optional[str] = None
    image_url: Optional[str] = None

    class Settings:
        name = "projects"

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Schema for User Input (When a student submits a project)
class ProjectCreate(BaseModel):
    title: str
    description: str
    team_members: List[str]
    github_link: Optional[str] = None
    demo_link: Optional[str] = None
    image_url: Optional[str] = None