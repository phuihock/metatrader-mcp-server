"""
MetaTrader 5 connection module.

This module provides functionality to connect to a MetaTrader 5 terminal.
"""
import os
import time
import datetime
import logging
import random
from typing import Dict, List, Tuple, Union, Optional

try:
    import MetaTrader5 as mt5
except ImportError:
    raise ImportError("MetaTrader5 package is not installed. Please install it with: pip install MetaTrader5")

from MetaTraderMCPServer.client.exceptions import ConnectionError, InitializationError, LoginError, DisconnectionError


# Set up logger
logger = logging.getLogger("MT5Connection")


class MT5Connection:
    """
    MetaTrader 5 connection class.
    
    This class provides functionality to connect to a MetaTrader 5 terminal.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize the MetaTrader 5 connection.
        
        Args:
            config: A dictionary containing the connection configuration.
                - path (str): Path to the MetaTrader 5 terminal executable (default: None).
                - login (int): Login ID (default: None).
                - password (str): Password (default: None).
                - server (str): Server name (default: None).
                - timeout (int): Timeout in milliseconds (default: 60000).
                - portable (bool): Whether to use portable mode (default: False).
                - debug (bool): Whether to enable debug logging (default: False).
                - max_retries (int): Maximum number of connection retries (default: 3).
                - backoff_factor (float): Backoff factor for retry delays (default: 1.5).
                - cooldown_time (float): Cooldown time between connections in seconds (default: 2.0).
        """
        self.config = config
        self.path = config.get("path")
        self.login = config.get("login")
        self.password = config.get("password")
        self.server = config.get("server")
        self.timeout = config.get("timeout", 60000)
        self.portable = config.get("portable", False)
        self.debug = config.get("debug", False)
        self.max_retries = config.get("max_retries", 3)
        self.backoff_factor = config.get("backoff_factor", 1.5)
        self.cooldown_time = config.get("cooldown_time", 2.0)
        self._connected = False
        self._last_connection_time = 0
        
        # Set up logging level
        if self.debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
        
        # Standard paths to look for MetaTrader 5 terminal
        self.standard_paths = [
            "C:\\Program Files\\MetaTrader 5\\terminal64.exe",
            "C:\\Program Files (x86)\\MetaTrader 5\\terminal.exe",
            os.path.expanduser("~\\AppData\\Roaming\\MetaQuotes\\Terminal\\*\\terminal64.exe"),
        ]
    
    def _find_terminal_path(self) -> str:
        """
        Find the MetaTrader 5 terminal path.
        
        Returns:
            str: Path to the MetaTrader 5 terminal.
        
        Raises:
            InitializationError: If the terminal path cannot be found.
        """
        if self.path and os.path.isfile(self.path):
            return self.path
        
        # Try standard paths
        for path in self.standard_paths:
            if '*' in path:
                # Handle wildcard paths
                import glob
                paths = glob.glob(path)
                if paths:
                    return paths[0]
            elif os.path.isfile(path):
                return path
        
        raise InitializationError("Could not find MetaTrader 5 terminal path")
    
    def _ensure_cooldown(self):
        """
        Ensure that there's a cooldown period between connection attempts
        to prevent rate limiting and authorization issues.
        """
        now = time.time()
        elapsed = now - self._last_connection_time
        
        if self._last_connection_time > 0 and elapsed < self.cooldown_time:
            cooldown_needed = self.cooldown_time - elapsed
            logger.debug(f"Applying cooldown of {cooldown_needed:.2f} seconds")
            time.sleep(cooldown_needed)
        
        self._last_connection_time = time.time()
    
    def _initialize_terminal(self) -> bool:
        """
        Initialize the MetaTrader 5 terminal.
        
        Returns:
            bool: True if successful, False otherwise.
        
        Raises:
            InitializationError: If initialization fails.
        """
        # Ensure proper cooldown between connection attempts
        self._ensure_cooldown()
        
        # Check if terminal is already initialized
        if mt5.terminal_info() is not None:
            logger.debug("Terminal is already initialized")
            return True
        
        # Find terminal path if not specified
        if not self.path:
            try:
                self.path = self._find_terminal_path()
                logger.debug(f"Found terminal path: {self.path}")
            except InitializationError:
                # If we can't find the path, try without specifying a path
                # MT5 will try to find the terminal itself
                self.path = None
                logger.debug("Could not find terminal path, trying without path")
        
        # Try to ensure login is an integer
        if self.login is not None:
            try:
                self.login = int(self.login)
            except ValueError:
                raise InitializationError(f"Invalid login format: {self.login}. Must be an integer.")
        
        # Print initialization parameters for debugging
        logger.debug(f"Attempting to initialize with path={self.path}")
        
        retries = 0
        while retries < self.max_retries:
            # Add small jitter to prevent exact same-time retries
            jitter = random.uniform(0, 0.5)
            
            try:
                result = mt5.initialize(
                    path=self.path,
                    login=self.login,
                    password=self.password,
                    server=self.server,
                    timeout=self.timeout,
                    portable=self.portable
                )
                
                if result:
                    return True
                
                error_code, error_message = self._get_last_error()
                # Handle specific error cases
                if error_code == -6:  # Authorization failed
                    logger.warning(f"Authorization failed (Error code: {error_code}). Cooling down before retry.")
                    # Longer cooldown for auth failures
                    time.sleep(self.cooldown_time * 2 + jitter)
                else:
                    # Regular backoff for other errors
                    backoff_time = self.backoff_factor ** retries + jitter
                    logger.warning(f"Initialization failed (Error code: {error_code}). Retrying in {backoff_time:.2f} seconds.")
                    time.sleep(backoff_time)
            except Exception as e:
                logger.error(f"Unexpected error during initialization: {str(e)}")
                backoff_time = self.backoff_factor ** retries + jitter
                time.sleep(backoff_time)
            
            retries += 1
        
        # If we got here, all retries failed
        error_code, error_message = self._get_last_error()
        raise InitializationError(f"Failed to initialize MetaTrader 5 terminal: {error_message} (Error code: {error_code})")
    
    def _login(self) -> bool:
        """
        Login to the MetaTrader 5 terminal.
        
        Returns:
            bool: True if successful, False otherwise.
        
        Raises:
            LoginError: If login fails.
        """
        # Check if we're already logged in
        if mt5.account_info() is not None:
            logger.debug("Already logged in")
            return True
        
        # Check if we need login credentials
        if self.login is None or self.password is None or self.server is None:
            # No credentials provided, but we're connected to the terminal
            # This could be a demo or already logged-in account
            if mt5.terminal_info() is not None:
                logger.debug("No login credentials provided, but terminal is initialized")
                return True
            else:
                raise LoginError("Login credentials not provided")
        
        logger.debug(f"Attempting to login with login={self.login}, server={self.server}")
        
        retries = 0
        while retries < self.max_retries:
            try:
                result = mt5.login(
                    login=self.login,
                    password=self.password,
                    server=self.server
                )
                
                if result:
                    logger.debug("Login successful!")
                    return True
                
                error_code, error_message = self._get_last_error()
                
                # Add a growing delay between retries (exponential backoff)
                backoff_time = self.backoff_factor ** retries + random.uniform(0, 0.5)
                logger.warning(f"Login failed: {error_message} (Error code: {error_code}). Retrying in {backoff_time:.2f} seconds.")
                time.sleep(backoff_time)
            except Exception as e:
                logger.error(f"Unexpected error during login: {str(e)}")
                backoff_time = self.backoff_factor ** retries + random.uniform(0, 0.5)
                time.sleep(backoff_time)
            
            retries += 1
        
        # If we got here, all retries failed
        error_code, error_message = self._get_last_error()
        raise LoginError(f"Failed to login to MetaTrader 5 terminal: {error_message} (Error code: {error_code})")
    
    def _get_last_error(self) -> Tuple[int, str]:
        """
        Get the last error from the MetaTrader 5 terminal.
        
        Returns:
            Tuple[int, str]: Error code and message.
        """
        if not hasattr(mt5, 'last_error'):
            return (-1, "Unknown error (mt5.last_error not available)")
        
        error = mt5.last_error()
        if error is None:
            return (0, "No error")
        
        try:
            code = error[0]
            message = error[1]
            return (code, message)
        except (IndexError, TypeError):
            return (-1, str(error))
    
    def connect(self) -> bool:
        """
        Connect to the MetaTrader 5 terminal.
        
        Returns:
            bool: True if successful, False otherwise.
        
        Raises:
            ConnectionError: If connection fails.
        """
        logger.debug("Attempting to connect to MetaTrader 5 terminal")
        
        try:
            # Initialize terminal
            self._initialize_terminal()
            
            # Login
            self._login()
            
            # Set connection flag
            self._connected = True
            logger.info("Successfully connected to MetaTrader 5 terminal")
            return True
        except (InitializationError, LoginError) as e:
            # Re-raise as ConnectionError
            self._connected = False
            raise ConnectionError(str(e)) from e
        except Exception as e:
            self._connected = False
            raise ConnectionError(f"Unexpected error: {str(e)}") from e
    
    def disconnect(self) -> bool:
        """
        Disconnect from the MetaTrader 5 terminal.
        
        Returns:
            bool: True if successful, False otherwise.
        
        Raises:
            DisconnectionError: If disconnection fails.
        """
        logger.debug("Attempting to disconnect from MetaTrader 5 terminal")
        
        if not self._connected:
            logger.debug("Already disconnected")
            return True
        
        try:
            result = mt5.shutdown()
            if result:
                self._connected = False
                logger.info("Successfully disconnected from MetaTrader 5 terminal")
                return True
            else:
                error_code, error_message = self._get_last_error()
                raise DisconnectionError(f"Failed to disconnect from MetaTrader 5 terminal: {error_message} (Error code: {error_code})")
        except Exception as e:
            if "not initialized" in str(e).lower():
                # Already disconnected
                self._connected = False
                logger.debug("Terminal already disconnected")
                return True
            raise DisconnectionError(f"Error disconnecting from MetaTrader 5 terminal: {str(e)}")
    
    def is_connected(self) -> bool:
        """
        Check if connected to the MetaTrader 5 terminal.
        
        Returns:
            bool: True if connected, False otherwise.
        """
        try:
            terminal_info = mt5.terminal_info()
            return terminal_info is not None and terminal_info._asdict().get('connected', False) and self._connected
        except Exception as e:
            logger.warning(f"Error checking connection status: {str(e)}")
            return False
    
    def get_terminal_info(self) -> Dict:
        """
        Get information about the MetaTrader 5 terminal.
        
        Returns:
            Dict: Terminal information.
        
        Raises:
            ConnectionError: If not connected to the terminal.
        """
        if not self.is_connected():
            raise ConnectionError("Not connected to MetaTrader 5 terminal")
        
        try:
            terminal_info = mt5.terminal_info()
            if terminal_info is not None:
                return terminal_info._asdict()
            else:
                error_code, error_message = self._get_last_error()
                raise ConnectionError(f"Could not get terminal info: {error_message} (Error code: {error_code})")
        except Exception as e:
            raise ConnectionError(f"Error getting terminal info: {str(e)}")
    
    def get_version(self) -> Tuple[int, int, int, int]:
        """
        Get the version of the MetaTrader 5 terminal.
        
        Returns:
            Tuple[int, int, int, int]: Version as (major, minor, build, revision).
        
        Raises:
            ConnectionError: If not connected to the terminal.
        """
        if not self.is_connected():
            raise ConnectionError("Not connected to MetaTrader 5 terminal")
        
        try:
            # Get terminal info which includes build number
            terminal_info = self.get_terminal_info()
            
            # Try to get build number directly
            build = terminal_info.get('build', 0)
            
            # Try alternative ways to get version information
            # Method 1: Use the name field which might include version
            name = terminal_info.get('name', '')
            name_version = name.split()[-1] if name and len(name.split()) > 1 else ''
            
            # Try to parse version from name
            major = minor = revision = 0
            if name_version:
                parts = name_version.split('.')
                if len(parts) >= 1:
                    try:
                        major = int(parts[0])
                    except (ValueError, IndexError):
                        pass
                if len(parts) >= 2:
                    try:
                        minor = int(parts[1])
                    except (ValueError, IndexError):
                        pass
                if len(parts) >= 3:
                    try:
                        revision = int(parts[2])
                    except (ValueError, IndexError):
                        pass
            
            # If we couldn't parse the version from the name, use defaults
            if major == 0:
                # MetaTrader 5, so major version is 5
                major = 5
            
            # Return the version tuple
            return (major, minor, build, revision)
        except Exception as e:
            raise ConnectionError(f"Error getting terminal version: {str(e)}")
