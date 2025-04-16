"""
MetaTrader 5 connection management module.
Handles establishing and maintaining connection to MT5 terminal.
"""
import time
import threading
from typing import Optional, Dict, Any
from mcp_server.core.config import settings
from mcp_server.core.logging_config import mt5_logger

# Import conditionally to handle environments where MT5 package isn't installed
try:
    from metatrader_client.client import MT5Client
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False
    mt5_logger.warning("MetaTrader client not available - import failed")

# Global MT5Client instance
mt5_client: Optional[Any] = None
_last_connection_attempt: float = 0
_connection_lock = threading.Lock()
_reconnect_interval = 60  # seconds between reconnection attempts

def initialize_mt5_client() -> bool:
    """Initialize the MT5 client and connect to the terminal.
    
    Returns:
        bool: True if successfully connected, False otherwise
    """
    global mt5_client, _last_connection_attempt
    
    if not MT5_AVAILABLE:
        mt5_logger.error("MT5 client not available - cannot initialize")
        return False
    
    with _connection_lock:
        # Skip if we're already connected
        if mt5_client and mt5_client.is_connected():
            mt5_logger.debug("MT5 already connected")
            return True
            
        # Check if we have credentials
        if not settings.has_mt5_credentials:
            mt5_logger.warning("MT5 credentials not configured - cannot connect")
            return False
        
        # Update last attempt time
        _last_connection_attempt = time.time()
        
        try:
            # Configure client
            config = {
                "login": settings.MT5_LOGIN,
                "password": settings.MT5_PASSWORD,
                "server": settings.MT5_SERVER,
            }
            
            # Add optional path if specified
            if settings.MT5_PATH:
                config["path"] = settings.MT5_PATH
                
            # Add debug flag if in debug mode
            if settings.DEBUG:
                config["debug"] = True
                
            # Create client instance
            mt5_client = MT5Client(config)
            
            # Connect to terminal
            connected = mt5_client.connect()
            
            if connected:
                mt5_logger.info(f"Successfully connected to MetaTrader terminal ({mt5_client.get_terminal_info()})")
                return True
            else:
                error = mt5_client.last_error()
                mt5_logger.error(f"Failed to connect to MetaTrader terminal: {error}")
                mt5_client = None
                return False
                
        except Exception as e:
            mt5_logger.exception(f"Error while connecting to MetaTrader: {str(e)}")
            mt5_client = None
            return False

def get_mt5_client() -> Optional[Any]:
    """Get the MT5 client instance, reconnecting if necessary.
    
    Returns:
        Optional[MT5Client]: The MT5 client instance, or None if not available
    """
    global mt5_client, _last_connection_attempt

    # Quick check without lock first
    if mt5_client and mt5_client.is_connected():
        return mt5_client
        
    # If we're not connected, try to reconnect (with backoff)
    with _connection_lock:
        # Check again within the lock
        if mt5_client and mt5_client.is_connected():
            return mt5_client
            
        # Respect reconnect interval
        current_time = time.time()
        if current_time - _last_connection_attempt < _reconnect_interval:
            return None
            
        # Try to reconnect
        if initialize_mt5_client():
            return mt5_client
        else:
            return None

def disconnect():
    """Disconnect from the MT5 terminal."""
    global mt5_client
    
    with _connection_lock:
        if mt5_client:
            mt5_client.disconnect()
            mt5_logger.info("Disconnected from MetaTrader terminal")
            mt5_client = None
