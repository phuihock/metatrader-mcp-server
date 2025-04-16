# MT5 Account Module Documentation 💰

## Overview 🌟

The `account` module provides comprehensive functionality for interacting with MetaTrader 5 trading accounts. It enables you to retrieve account information, check balance and margin levels, verify trading permissions, and obtain trade statistics. This module is built on top of the connection module and provides a robust, error-handled interface to the MT5 platform's account operations.

## Quick Start Guide 🚀

```python
from metatrader_client.connection import MT5Connection
from metatrader_client.account import MT5Account

# Set up configuration
config = {
    "login": 12345678,  # Your MT5 account number
    "password": "your-password",
    "server": "Your-Broker-Server",
    "debug": True  # Enable debug logging
}

# Create connection and account objects
connection = MT5Connection(config)
account = MT5Account(connection)

try:
    # Connect to terminal
    connection.connect()
    print("✅ Connected to MetaTrader 5!")
    
    # Get basic account information
    account_info = account.get_account_info()
    print(f"Account: {account_info['login']} ({account.get_account_type()})")
    print(f"Balance: {account.get_balance()} {account.get_currency()}")
    print(f"Equity: {account.get_equity()} {account.get_currency()}")
    print(f"Leverage: 1:{account.get_leverage()}")
    
    # Check if trading is allowed
    if account.is_trade_allowed():
        print("✅ Trading is allowed")
    else:
        print("❌ Trading is not allowed")
    
    # Check margin level
    try:
        if account.check_margin_level(min_level=100.0):
            print("✅ Margin level is sufficient")
    except MarginLevelError as e:
        print(f"❌ {str(e)}")
    
    # Get trade statistics
    stats = account.get_trade_statistics()
    print(f"Profit: {stats['profit']} {stats['currency']}")
    print(f"Free Margin: {stats['free_margin']} {stats['currency']}")
    
    # Disconnect when done
    connection.disconnect()
    print("✅ Disconnected from MetaTrader 5")
    
except Exception as e:
    print(f"❌ Error: {e}")
```

## Detailed Documentation 📖

### Account Class Structure 🏗️

The `MT5Account` class is the main component of this module and provides the following structure:

#### Constructor

```python
MT5Account(connection: MT5Connection)
```

Creates a new account manager using an existing connection to the MT5 terminal.

**Parameters:**
- `connection`: An instance of MT5Connection that is used to communicate with the terminal

### Key Methods 🔑

#### Account Information

##### `get_account_info()` 📊
```python
get_account_info() -> Dict[str, Any]
```
Retrieves comprehensive account information from the MT5 terminal.

**Returns:**
- `Dict[str, Any]`: Dictionary containing all account properties including login, balance, equity, margin, currency, etc.

**Raises:**
- `AccountInfoError`: If account information cannot be retrieved
- `ConnectionError`: If not connected to terminal

##### `get_balance()` 💵
```python
get_balance() -> float
```
Gets the current account balance (without considering open positions).

**Returns:**
- `float`: Current account balance

**Raises:**
- `AccountInfoError`: If balance cannot be retrieved
- `ConnectionError`: If not connected to terminal

##### `get_equity()` 📈
```python
get_equity() -> float
```
Gets the current equity (balance plus floating profit/loss from open positions).

**Returns:**
- `float`: Current account equity

**Raises:**
- `AccountInfoError`: If equity cannot be retrieved
- `ConnectionError`: If not connected to terminal

##### `get_margin()` 📉
```python
get_margin() -> float
```
Gets the current used margin (amount reserved for open positions).

**Returns:**
- `float`: Current used margin

**Raises:**
- `AccountInfoError`: If margin cannot be retrieved
- `ConnectionError`: If not connected to terminal

##### `get_free_margin()` 🆓
```python
get_free_margin() -> float
```
Gets the current free margin (amount available for opening new positions).

**Returns:**
- `float`: Current free margin

**Raises:**
- `AccountInfoError`: If free margin cannot be retrieved
- `ConnectionError`: If not connected to terminal

##### `get_margin_level()` 📊
```python
get_margin_level() -> float
```
Gets the current margin level as a percentage (Equity/Margin * 100%).

**Returns:**
- `float`: Current margin level in percentage

**Raises:**
- `AccountInfoError`: If margin level cannot be retrieved
- `ConnectionError`: If not connected to terminal

##### `get_currency()` 💱
```python
get_currency() -> str
```
Gets the account currency.

**Returns:**
- `str`: Account currency code (e.g., "USD", "EUR")

**Raises:**
- `AccountInfoError`: If currency cannot be retrieved
- `ConnectionError`: If not connected to terminal

##### `get_leverage()` 📊
```python
get_leverage() -> int
```
Gets the account leverage.

**Returns:**
- `int`: Account leverage (e.g., 100 for 1:100 leverage)

**Raises:**
- `AccountInfoError`: If leverage cannot be retrieved
- `ConnectionError`: If not connected to terminal

#### Account Status

##### `get_account_type()` 🏦
```python
get_account_type() -> str
```
Gets the account type.

**Returns:**
- `str`: Account type ("real", "demo", or "contest")

**Raises:**
- `AccountInfoError`: If account type cannot be retrieved
- `ConnectionError`: If not connected to terminal

##### `is_trade_allowed()` ✅
```python
is_trade_allowed() -> bool
```
Checks if trading is allowed for this account.

**Returns:**
- `bool`: True if trading is allowed, False otherwise

**Raises:**
- `AccountInfoError`: If trading permission cannot be determined
- `ConnectionError`: If not connected to terminal

##### `check_margin_level()` ⚠️
```python
check_margin_level(min_level: float = 100.0) -> bool
```
Checks if margin level is above the specified minimum level.

**Parameters:**
- `min_level`: Minimum margin level in percentage (default: 100.0)

**Returns:**
- `bool`: True if margin level is above the minimum

**Raises:**
- `MarginLevelError`: If margin level is below the minimum
- `AccountInfoError`: If margin level cannot be retrieved
- `ConnectionError`: If not connected to terminal

#### Statistics and Analysis

##### `get_trade_statistics()` 📊
```python
get_trade_statistics() -> Dict[str, Any]
```
Gets basic trade statistics for the account.

**Returns:**
- `Dict[str, Any]`: Dictionary with trade statistics including:
  - balance: Current balance
  - equity: Current equity
  - profit: Current floating profit/loss
  - margin_level: Current margin level
  - free_margin: Available margin for trading
  - account_type: Account type
  - leverage: Account leverage
  - currency: Account currency

**Raises:**
- `AccountInfoError`: If statistics cannot be retrieved
- `ConnectionError`: If not connected to terminal

## Robust Error Handling ⚠️

The module includes specialized exceptions for different error scenarios:

- `AccountError`: Base exception for all account-related issues
- `AccountInfoError`: When account information cannot be retrieved
- `TradingNotAllowedError`: When trading operations are not allowed
- `MarginLevelError`: When margin level is below the required minimum

## Advanced Features 🛠️

### Smart Error Handling 🔄

1. **Detailed Error Messages** - All errors include specific information about what went wrong
2. **Type-Specific Exceptions** - Different errors trigger specific exception types for easier handling
3. **Margin Level Protection** - Automatic checking of margin levels before operations

### Comprehensive Account Information 📝

The account module provides access to all account properties, making it easy to:

1. **Monitor account status** - Track equity, balance, and margin in real-time
2. **Verify trading permissions** - Check if trading is allowed
3. **Analyze account performance** - Get profit/loss and other statistics

### Logging 📝

When debug mode is enabled, the module logs detailed information about account operations, including:

- Account information retrieval attempts
- Trading permission checks
- Margin level checks
- Error conditions and details

## Testing ✅

The account module includes comprehensive tests to ensure reliability and stability:

### Unit Tests (with Mocks)

- Account information retrieval
- Property getters (balance, equity, margin, etc.)
- Account type determination
- Trade allowed status
- Margin level checks
- Trade statistics retrieval
- Error handling

### Integration Tests (with Real MT5 Connection)

- Real account information retrieval
- Real-time property values
- Actual margin level checks
- Actual trading permission verification

### Edge Case Tests

- Zero margin level handling
- No connection scenario

### Running Tests

```bash
# Run account tests with mocks
python -m tests.run_tests account

# Run simple account test
python -m tests.run_tests simple

# Run all tests including integration tests
python -m tests.run_tests all
```

## Troubleshooting 🔍

### Common Issues and Solutions

#### "Failed to retrieve account information"

- Ensure you are connected to the terminal
- Verify your network connection
- Check if the terminal is responsive
- Restart the MetaTrader 5 terminal if needed

#### "Margin level too low"

- Close some positions to reduce margin usage
- Add more funds to your account
- Reduce position sizes on new trades
- Use lower leverage if possible

#### "Trading not allowed"

- Check if your account is activated
- Verify if the market is open
- Check if automated trading is enabled in terminal settings
- Ensure your account has sufficient funds

#### "Not connected to MetaTrader 5 terminal"

- Ensure the connection is established before account operations
- Verify that the MT5 terminal is running
- Check the connection status with `is_connected()`

## Best Practices 💡

1. **Check connection status first** - Always verify connection before account operations
2. **Verify margin level** - Check margin level before placing trades
3. **Handle exceptions properly** - Use try/except blocks around account operations
4. **Monitor account statistics regularly** - Track balance, equity, and margin levels
5. **Check trading permission** - Verify trading is allowed before attempting trades
6. **Use debug logging** - Enable debug mode for detailed logging during development

## Further Resources 📚

- [MetaTrader 5 Python Documentation](https://www.mql5.com/en/docs/python_metatrader5)
- [MetaTrader 5 Account Properties](https://www.mql5.com/en/docs/constants/environment_state/accountinformation)
- [Connection Module Documentation](./connection.md) for establishing MT5 connections
- [Project README](../../README.md) for overall project information

---

*This documentation was last updated on April 10, 2025.*
