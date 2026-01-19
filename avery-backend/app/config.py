import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/avery"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    anthropic_api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
