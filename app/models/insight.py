from beanie import Document, PydanticObjectId
from pydantic import BaseModel
from typing import Optional

class Insight(Document):
    # --- Dynamic Data ---
    personName: str
    description: str  
    image: Optional[str] = None
    
    # NEW FIELD: Instagram Profile Link
    insta_link: Optional[str] = None 
    
    # --- Fixed / Styling Data ---
    title: str = "Insight Series"
    bgColor: str = "rgba(125, 212, 238, 0.15)"
    borderColor: str = "#7dd4ee"
    size: str = "regular"
    year:Optional[str]="Alumni"
    class Settings:
        name = "insights"

# Schema for CREATING
class InsightCreate(BaseModel):
    personName: str
    description: str
    image: Optional[str] = None
    insta_link: Optional[str] = None 
    
    # ✅ ADDED: Missing styling fields
    title: Optional[str] = "Insight Series"
    bgColor: Optional[str] = "rgba(125, 212, 238, 0.15)"
    borderColor: Optional[str] = "#7dd4ee"
    size: Optional[str] = "regular"

# Schema for UPDATING
class InsightUpdate(BaseModel):
    personName: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    insta_link: Optional[str] = None 
    
    # ✅ ADDED: Missing styling fields
    title: Optional[str] = None
    bgColor: Optional[str] = None
    borderColor: Optional[str] = None
    size: Optional[str] = None