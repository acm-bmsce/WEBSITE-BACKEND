import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # Update this line to match your .env variable name if you prefer 'mongo_uri'
    # But standardizing on MONGO_URL is recommended.
    MONGO_URL: str 

    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback_secret")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    class Config:
        env_file = ".env"
        # This tells Pydantic to ignore extra fields in .env (like 'mongo_uri' if unused)
        extra = "ignore" 

settings = Settings()