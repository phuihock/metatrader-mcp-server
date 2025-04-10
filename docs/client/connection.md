# MT5 Connection Module Documentation 🔌

## Overview 🌟

The `connection` module is the foundation of the MetaTrader MCP Server client interface. It provides robust functionality for establishing, managing, and monitoring connections to the MetaTrader 5 terminal. This module ensures reliable communication between your Python code and the MetaTrader platform.

## Quick Start Guide 🚀

```python
from MetaTraderMCPServer.client.connection import MT5Connection

# Set up configuration
config = {
    "login": 12345678,  # Your MT5 account number (as integer)
    "password": "your-password",
    "server": "Your-Broker-Server",
    # Optional parameters:
    "path": "C:\\Program Files\\MetaTrader 5\\terminal64.exe",  # Optional: Auto-detected if not provided
    "timeout": 60000,  # Connection timeout in milliseconds
    "portable": False,  # Whether to use portable mode
    "debug": True,      # Enable debug logging
    "max_retries": 3,   # Maximum number of connection retries
    "cooldown_time": 2.0  # Cooldown time between connections in seconds
}

# Create connection object
mt5_connection = MT5Connection(config)

# Connect to terminal
try:
    mt5_connection.connect()
    print("✅ Connected to MetaTrader 5!")
    
    # Get terminal information
    terminal_info = mt5_connection.get_terminal_info()
    print(f"Terminal version: {mt5_connection.get_version()}")
    print(f"Connected: {mt5_connection.is_connected()}")
    
    # When finished, disconnect properly
    mt5_connection.disconnect()
    print("✅ Disconnected from MetaTrader 5")
    
except Exception as e:
    print(f"❌ Error: {e}")
```

## Detailed Documentation 📖

### Connection Class Structure 🏗️

The `MT5Connection` class is the main component of this module and provides the following structure:

#### Constructor

```python
MT5Connection(config: Dict)
```

Creates a new connection manager with specified configuration.

**Parameters:**
- `config`: Dictionary with the following keys:
  - `path` (str, optional): Path to the MT5 terminal executable
  - `login` (int): Account login ID
  - `password` (str): Account password
  - `server` (str): Server name
  - `timeout` (int, optional): Connection timeout in milliseconds (default: 60000)
  - `portable` (bool, optional): Whether to use portable mode (default: False)
  - `debug` (bool, optional): Enable debug logging (default: False)
  - `max_retries` (int, optional): Maximum number of connection retries (default: 3)
  - `backoff_factor` (float, optional): Backoff factor for retry delays (default: 1.5)
  - `cooldown_time` (float, optional): Cooldown time between connections in seconds (default: 2.0)

### Key Methods 🔑

#### Connection Management

##### `connect()` 🔌
```python
connect() -> bool
```
Establishes a connection to the MetaTrader 5 terminal. If the terminal is not running, it will attempt to start it automatically.

**Returns:**
- `bool`: True if connection was successful

**Raises:**
- `ConnectionError`: If connection fails for any reason
- `InitializationError`: If terminal initialization fails
- `LoginError`: If login fails with provided credentials

##### `disconnect()` 🔌
```python
disconnect() -> bool
```
Properly closes the connection to the MetaTrader 5 terminal.

**Returns:**
- `bool`: True if disconnection was successful

**Raises:**
- `DisconnectionError`: If disconnection fails

##### `is_connected()` ✅
```python
is_connected() -> bool
```
Checks if the connection to the terminal is active.

**Returns:**
- `bool`: True if connected, False otherwise

#### Information Retrieval

##### `get_terminal_info()` 📊
```python
get_terminal_info() -> Dict
```
Retrieves comprehensive information about the connected terminal.

**Returns:**
- `Dict`: Dictionary containing terminal information such as build, path, version, etc.

**Raises:**
- `ConnectionError`: If not connected to terminal

##### `get_version()` 📋
```python
get_version() -> Tuple[int, int, int, int]
```
Gets the version of the connected terminal.

**Returns:**
- `Tuple[int, int, int, int]`: Version as (major, minor, build, revision)

**Raises:**
- `ConnectionError`: If not connected to terminal

### Internal Methods 🔧

These methods are used internally but are not typically called directly:

- `_find_terminal_path()`: Locates the MT5 terminal executable
- `_ensure_cooldown()`: Manages cooldown periods between connection attempts
- `_initialize_terminal()`: Initializes the terminal connection
- `_login()`: Performs login after initialization
- `_get_last_error()`: Retrieves the last error from the terminal

## Robust Error Handling ⚠️

The module includes specialized exceptions for different error scenarios:

- `ConnectionError`: Base exception for all connection issues
- `InitializationError`: When terminal initialization fails
- `LoginError`: When login fails with provided credentials
- `DisconnectionError`: When disconnection fails

## Advanced Features 🛠️

### Auto-Recovery 🔄

The connection module implements several reliability features:

1. **Automatic Terminal Detection** - If no path is provided, the module will search standard installation locations
2. **Retry Logic** - Implements exponential backoff with jitter for more reliable connections
3. **Connection Cooldown** - Prevents rate limiting by ensuring adequate time between connection attempts
4. **Error-Specific Handling** - Special handling for different types of errors (e.g., authentication failures)

### Logging 📝

When debug mode is enabled, the module logs detailed information about connection attempts, failures, and success. This is useful for troubleshooting connection issues.

## Testing ✅

The connection module includes comprehensive tests to ensure reliability and stability:

### Basic Tests

- Connection establishment and status verification
- Terminal information retrieval
- Version information retrieval
- Proper disconnection

### Edge Case Tests

- Invalid path handling
- Invalid login format detection
- Multiple reconnection cycles
- Very short timeout values

### Stress Tests

- Rapid connect/disconnect cycles
- Recovery after abnormal termination

### Security Tests

- Credential privacy in error messages

### Running Tests

```bash
# Run simple connection test
python tests/client/connection.py

# Run all tests including edge cases
python tests/run_tests.py

# Run only long-running tests
python tests/run_tests.py long
```

## Troubleshooting 🔍

### Common Issues and Solutions

#### "Could not find MetaTrader 5 terminal path"

- Ensure MetaTrader 5 is installed on your system
- Provide the explicit path to terminal64.exe in the config
- Check if the terminal is accessible by the user running the script

#### "Authorization failed"

- Verify your login credentials
- Confirm the server name is correct
- Check if your account is active
- Ensure your IP is not blocked by the broker

#### "Terminal not responding"

- Restart the MetaTrader 5 terminal
- Check if another process is already connected to the terminal
- Increase the timeout value in your configuration

#### "Timeout error"

- Increase the timeout value in your configuration
- Check your network connection
- Verify the MetaTrader terminal is responsive

## Best Practices 💡

1. **Always disconnect properly** - Call `disconnect()` when finished to release resources
2. **Use a context manager pattern** if possible for automatic cleanup
3. **Handle exceptions** - Wrap connection code in try/except blocks
4. **Check connection status** - Call `is_connected()` before operations
5. **Use cooldown periods** - Don't hammer the terminal with rapid connections
6. **Secure credentials** - Don't hardcode login information; use environment variables

## Further Resources 📚

- [MetaTrader 5 Python Documentation](https://www.mql5.com/en/docs/python_metatrader5)
- [Project README](../../README.md) for overall project information

---

*This documentation was last updated on April 10, 2025.*
