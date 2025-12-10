from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
# Import all your models
from app.models.event import Event
from app.models.project import Project
from app.models.user import User
from app.models.insight import Insight
from app.config import settings  # ✅ Import Settings

async def init_db():
    # ✅ Use the variable from config
    client = AsyncIOMotorClient(settings.MONGO_URL)
    
    await init_beanie(
        database=client.acm_website_db,
        document_models=[
            Event,
            Project,
            User,
            Insight
        ]
    )