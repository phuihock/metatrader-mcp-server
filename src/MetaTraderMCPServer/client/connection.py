"""
MetaTrader 5 connection management module.

This module handles establishing, monitoring, and closing connections to the MT5 terminal.
"""
from typing import Dict, Any, Optional, Tuple
from .exceptions import ConnectionError


class MT5Connection:
    """
    Manages connection to the MetaTrader 5 terminal.
    
    Handles initialization, status checking, and proper termination of the connection.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the MT5 connection manager.
        
        Args:
            config: Optional configuration dictionary with connection parameters.
                   Can include: path, login, password, server, timeout, portable
        """
        self._config = config or {}
        self._connected = False
    
    def connect(self) -> bool:
        """
        Establish connection to the MetaTrader 5 terminal.
        
        If login credentials are provided in config, also performs login.
        Terminal is automatically launched if needed.
        
        Returns:
            bool: True if connection was successful, False otherwise.
            
        Raises:
            ConnectionError: If connection fails with specific error details.
        """
        pass
    
    def disconnect(self) -> bool:
        """
        Disconnect from the MetaTrader 5 terminal.
        
        Properly shuts down the connection to release resources.
        
        Returns:
            bool: True if disconnection was successful, False otherwise.
        """
        pass
    
    def is_connected(self) -> bool:
        """
        Check if the connection to MT5 terminal is active.
        
        Returns:
            bool: True if connected, False otherwise.
        """
        pass
    
    def get_terminal_info(self) -> Dict[str, Any]:
        """
        Get information about the connected MT5 terminal.
        
        Returns comprehensive information about the terminal including
        version, path, memory usage, etc.
        
        Returns:
            Dict[str, Any]: Terminal information.
            
        Raises:
            ConnectionError: If not connected to terminal.
        """
        pass
    
    def get_version(self) -> Tuple[int, int, int, int]:
        """
        Get the version of the connected MetaTrader 5 terminal.
        
        Returns:
            Tuple[int, int, int, int]: Version as (major, minor, build, revision).
            
        Raises:
            ConnectionError: If not connected to terminal.
        """
        pass
    
    def last_error(self) -> Tuple[int, str]:
        """
        Get the last error code and description.
        
        Returns:
            Tuple[int, str]: Error code and description.
        """
        pass
