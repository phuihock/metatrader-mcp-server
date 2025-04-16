from pydantic_settings import BaseSettings
import os
from pathlib import Path
from typing import Optional

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

class Settings(BaseSettings):
    # Server settings
    ENV: str = os.getenv("MCP_ENV", "development")
    DEBUG: bool = ENV == "development"
    LOG_LEVEL: str = "DEBUG" if DEBUG else "INFO"
    
    # Logging settings
    LOG_DIR: Path = PROJECT_ROOT / "logs"
    LOG_MAX_SIZE: int = 10 * 1024 * 1024  # 10 MB
    LOG_BACKUP_COUNT: int = 5
    SERVER_NAME: str = "MetaTrader MCP Server"
    
    # MetaTrader connection settings
    MT5_LOGIN: Optional[str] = None
    MT5_PASSWORD: Optional[str] = None
    MT5_SERVER: Optional[str] = None
    MT5_PATH: Optional[str] = None
    
    # MCP Tool settings
    ENABLE_DEMO_TOOLS: bool = True  # Set to False in production to disable demo tools
    ENABLE_TRADING_TOOLS: bool = True  # Can be disabled for read-only mode
    
    # Define aliases for MetaTrader fields
    login: Optional[str] = None
    password: Optional[str] = None
    server: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"  # Allow extra fields to be provided

    @property
    def has_mt5_credentials(self) -> bool:
        """Check if all required MT5 credentials are provided."""
        return all([self.MT5_LOGIN, self.MT5_PASSWORD, self.MT5_SERVER])

settings = Settings()
