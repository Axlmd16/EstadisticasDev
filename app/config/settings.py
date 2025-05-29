import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Settings(BaseSettings):
    MONGO_URL: str = os.getenv("MONGO_URL")
    REDIS_URL: str = os.getenv("REDIS_URL")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS")
    TIMEZONE: str = os.getenv("TIMEZONE")

settings = Settings()
