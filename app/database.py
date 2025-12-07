import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.event import Event
from app.models.project import Project
from app.models.user import User
from dotenv import load_dotenv

load_dotenv()

async def init_db():
    # Get URI from .env file
    mongo_uri = os.getenv("MONGO_URI")
    
    client = AsyncIOMotorClient(mongo_uri)
    
    # Define your database name here (e.g., "club_website")
    database = client.club_website 
    
    # Initialize Beanie with the Event model
    await init_beanie(database, document_models=[Event,Project,User])