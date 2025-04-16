import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from mcp_server.core.config import settings

# Create loggers for different components
mcp_logger = logging.getLogger('mcp')
mt5_logger = logging.getLogger('metatrader')
tools_logger = logging.getLogger('tools')

def setup_logging():
    """Set up logging for the MCP server.
    
    Configures separate loggers for MCP server, MetaTrader client,
    and tool operations with appropriate formatting.
    
    Logs are written to both the console and rotating log files.
    """
    # Ensure log directory exists
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    
    # Set the root logger level
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)
    
    # Clear any existing handlers (to avoid duplicates on reload)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # 1. Create console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(settings.LOG_LEVEL)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 2. Create main rotating file handler
    main_log_file = settings.LOG_DIR / "mcp.log"
    file_handler = RotatingFileHandler(
        main_log_file,
        maxBytes=settings.LOG_MAX_SIZE,
        backupCount=settings.LOG_BACKUP_COUNT
    )
    file_handler.setLevel(settings.LOG_LEVEL)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # 3. Create component-specific log files
    components = {
        "mcp": mcp_logger,
        "metatrader": mt5_logger,
        "tools": tools_logger
    }
    
    for name, logger in components.items():
        # Set logger level
        logger.setLevel(settings.LOG_LEVEL)
        
        # Create component log file
        component_log_file = settings.LOG_DIR / f"{name}.log"
        component_handler = RotatingFileHandler(
            component_log_file,
            maxBytes=settings.LOG_MAX_SIZE,
            backupCount=settings.LOG_BACKUP_COUNT
        )
        component_handler.setLevel(settings.LOG_LEVEL)
        component_handler.setFormatter(formatter)
        logger.addHandler(component_handler)
    
    # Log startup information
    mcp_logger.info(f"Starting {settings.SERVER_NAME} in {settings.ENV} mode")
    mcp_logger.info(f"Log files will be stored in: {settings.LOG_DIR}")
    if settings.DEBUG:
        mcp_logger.debug("Debug mode enabled")
