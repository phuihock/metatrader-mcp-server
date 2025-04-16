from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    ENV: str = os.getenv("MCP_ENV", "development")
    DEBUG: bool = ENV == "development"
    LOG_LEVEL: str = "DEBUG" if DEBUG else "INFO"
    login: str = ""
    password: str = ""
    server: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
