# MT5 Market Module Documentation 📊

## Overview 🌟

The `market` module provides comprehensive functionality for accessing market data in MetaTrader 5. It allows you to retrieve symbol information, current prices, and historical candle data for technical analysis and trading decisions. This module is essential for any trading strategy that requires real-time or historical market data.

## Quick Start Guide 🚀

```python
from metatrader_client import MT5Client

# Set up configuration
config = {
    "login": 12345678,  # Your MT5 account number
    "password": "your-password",
    "server": "Your-Broker-Server"
}

# Create client and connect
client = MT5Client(config)
client.connect()

# Access market functionality through the client's market property
try:
    # Get available symbols
    symbols = client.market.get_symbols("*USD*")
    print(f"Available USD pairs: {symbols[:5]}")
    
    # Get current price for EURUSD
    price = client.market.get_symbol_price("EURUSD")
    print(f"EURUSD - Bid: {price['bid']}, Ask: {price['ask']}")
    
    # Get detailed symbol information
    info = client.market.get_symbol_info("EURUSD")
    print(f"EURUSD spread: {info['spread']} points")
    
    # Get the latest 100 hourly candles for EURUSD
    candles = client.market.get_candles_latest("EURUSD", "H1")
    print(f"Latest close price: {candles['close'].iloc[0]}")
    
    # Get historical candles for a specific date range
    historical = client.market.get_candles_by_date(
        "EURUSD", "H1", 
        "2023-01-01 00:00", 
        "2023-01-31 23:59"
    )
    print(f"Retrieved {len(historical)} historical candles")
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    # Always disconnect when done
    client.disconnect()
```

## Detailed Documentation 📖

### Market Class Structure 🏗️

The `MT5Market` class is accessed through the `market` property of the `MT5Client` instance and provides the following functionality:

#### Constructor

```python
MT5Market(connection)
```

Creates a new market operations handler with the specified connection.

**Parameters:**
- `connection`: MT5Connection instance for terminal communication

### Key Methods 🔑

#### Symbol Information

##### `get_symbols(group: Optional[str] = None)` 🔍
```python
get_symbols(group: Optional[str] = None) -> List[str]
```
Get list of all available market symbols, optionally filtered by a pattern.

**Parameters:**
- `group` (str, optional): Filter symbols by group pattern (e.g., "\*USD\*" for USD pairs)
  - Wildcards can be used
  - Examples:
    - "\*" - all symbols
    - "EUR\*" - all symbols starting with EUR
    - "\*USD\*" - all symbols containing USD
    - "EUR\*,GBP\*" - all symbols starting with EUR or GBP

**Returns:**
- `List[str]`: List of symbol names matching the filter criteria

**Raises:**
- `MarketError`: If symbols cannot be retrieved due to API errors
- `ConnectionError`: If not connected to terminal or connection is lost

##### `get_symbol_info(symbol_name: str)` 📋
```python
get_symbol_info(symbol_name: str) -> Dict[str, Any]
```
Get detailed information about a specific symbol.

**Parameters:**
- `symbol_name` (str): Symbol name (e.g., "EURUSD", "XAUUSD")

**Returns:**
- `Dict[str, Any]`: Dictionary with comprehensive symbol information including:
  - `name` (str): Symbol name
  - `description` (str): Description of the symbol
  - `currency_base` (str): Base currency of the symbol
  - `currency_profit` (str): Profit currency of the symbol
  - `bid` (float): Current Bid price
  - `ask` (float): Current Ask price
  - `spread` (int): Spread value in points
  - `point` (float): Point size in the quote currency
  - `digits` (int): Number of decimal places in the symbol's price
  - `trade_contract_size` (float): Contract size per lot
  - And many more technical parameters...

**Raises:**
- `SymbolNotFoundError`: If symbol is invalid or not found
- `MarketError`: If symbol information cannot be retrieved
- `ConnectionError`: If not connected to terminal

#### Price Data

##### `get_symbol_price(symbol_name: str)` 💰
```python
get_symbol_price(symbol_name: str) -> Dict[str, Any]
```
Get current price for a symbol.

**Parameters:**
- `symbol_name` (str): Symbol name (e.g., "EURUSD", "XAUUSD")

**Returns:**
- `Dict[str, Any]`: Dictionary with price information:
  - `bid` (float): Current bid price (best sell offer)
  - `ask` (float): Current ask price (best buy offer)
  - `last` (float): Last deal price
  - `volume` (float): Volume for the current last price
  - `time` (datetime): Time of the last price update as datetime object in UTC timezone

**Raises:**
- `SymbolNotFoundError`: If symbol is invalid or not found
- `MarketDataError`: If price data cannot be retrieved

#### Historical Data

##### `get_candles_latest(symbol_name: str, timeframe: str, count: int = 100)` 📈
```python
get_candles_latest(symbol_name: str, timeframe: str, count: int = 100) -> pd.DataFrame
```
Get the latest candles for a symbol as a pandas DataFrame.

**Parameters:**
- `symbol_name` (str): Symbol name (e.g., "EURUSD", "XAUUSD")
- `timeframe` (str): Timeframe string (e.g., "M1", "H1"). Case-insensitive.
  - Common values:
    - "M1", "M5", "M15", "M30" - minutes
    - "H1", "H4" - hours
    - "D1" - daily
    - "W1" - weekly
    - "MN1" - monthly
- `count` (int, optional): Number of candles to retrieve (default: 100)

**Returns:**
- `pd.DataFrame`: DataFrame with OHLCV data:
  - `time`: Candle timestamp with UTC timezone
  - `open`: Open price
  - `high`: High price
  - `low`: Low price
  - `close`: Close price
  - `tick_volume`: Tick volume
  - `spread`: Spread
  - `real_volume`: Real volume (if available)

**Raises:**
- `SymbolNotFoundError`: If symbol is invalid or not found
- `InvalidTimeframeError`: If timeframe is invalid
- `MarketDataError`: If candle data cannot be retrieved
- `ConnectionError`: If not connected to terminal

##### `get_candles_by_date(symbol_name: str, timeframe: str, from_date: Optional[str] = None, to_date: Optional[str] = None)` 📅
```python
get_candles_by_date(symbol_name: str, timeframe: str, from_date: Optional[str] = None, to_date: Optional[str] = None) -> pd.DataFrame
```
Get historical price data (OHLCV) for a symbol between specified dates.

**Parameters:**
- `symbol_name` (str): Symbol name (e.g., "EURUSD", "XAUUSD")
- `timeframe` (str): Timeframe string (e.g., "M1", "H1"). Case-insensitive.
- `from_date` (str, optional): Start date in "yyyy-MM-dd HH:mm" format in UTC
- `to_date` (str, optional): End date in "yyyy-MM-dd HH:mm" format in UTC

The method is flexible with date parameters:
- If both dates are provided: returns data between those dates
- If only from_date is provided: returns data from that date to the present (limited to 1000 candles)
- If only to_date is provided: returns data for 30 days before that date
- If no dates are provided: returns the most recent 1000 candles

**Returns:**
- `pd.DataFrame`: DataFrame with OHLCV data sorted by newest to oldest:
  - `time`: Candle timestamp with UTC timezone
  - `open`: Open price
  - `high`: High price
  - `low`: Low price
  - `close`: Close price
  - `tick_volume`: Tick volume
  - `spread`: Spread
  - `real_volume`: Real volume (if available)

**Raises:**
- `SymbolNotFoundError`: If symbol is invalid or not found
- `InvalidTimeframeError`: If timeframe is invalid
- `MarketDataError`: If historical data cannot be retrieved
- `ValueError`: If date format is invalid or if to_date is earlier than from_date

## Advanced Usage 🛠️

### Timeframe Handling

The market module uses the `Timeframe` class from the `types` module to handle timeframe conversions. This allows you to use human-readable timeframe strings (like "M1", "H1") instead of MetaTrader's numeric constants.

```python
from metatrader_client.types import Timeframe

# Convert timeframe string to MT5 constant
mt5_timeframe = Timeframe["H1"]  # Gets the MT5 constant for 1-hour timeframe
```

### Working with Pandas DataFrames

The candle data methods return pandas DataFrames, which provide powerful data analysis capabilities:

```python
# Get hourly candles for EURUSD
candles = client.market.get_candles_latest("EURUSD", "H1", 100)

# Calculate simple moving average
candles['sma20'] = candles['close'].rolling(window=20).mean()

# Filter candles by condition
bullish_candles = candles[candles['close'] > candles['open']]

# Get basic statistics
stats = candles['close'].describe()
print(stats)
```

### Error Handling

The market module provides specific exception types for different error scenarios:

```python
from metatrader_client.exceptions import (
    SymbolNotFoundError, InvalidTimeframeError, MarketDataError
)

try:
    # Try to get data for a symbol
    candles = client.market.get_candles_latest("INVALID_SYMBOL", "H1")
except SymbolNotFoundError as e:
    print(f"Symbol not found: {e}")
except InvalidTimeframeError as e:
    print(f"Invalid timeframe: {e}")
except MarketDataError as e:
    print(f"Market data error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices 💡

1. **Always check symbol existence** before requesting detailed information or candles
2. **Use appropriate timeframes** for your analysis needs (smaller timeframes generate more data)
3. **Limit the amount of historical data** requested to improve performance
4. **Handle timezone differences** carefully (all times are returned in UTC)
5. **Implement proper error handling** for robust applications
6. **Disconnect from MT5** when your operations are complete

## Example: Simple Moving Average Crossover 📉

```python
import pandas as pd
import matplotlib.pyplot as plt
from metatrader_client import MT5Client

# Connect to MT5
client = MT5Client(config)
client.connect()

try:
    # Get 200 daily candles for EURUSD
    candles = client.market.get_candles_latest("EURUSD", "D1", 200)
    
    # Calculate moving averages
    candles['sma50'] = candles['close'].rolling(window=50).mean()
    candles['sma200'] = candles['close'].rolling(window=200).mean()
    
    # Identify crossover points
    candles['crossover'] = (candles['sma50'] > candles['sma200']) & (candles['sma50'].shift(1) <= candles['sma200'].shift(1))
    candles['crossunder'] = (candles['sma50'] < candles['sma200']) & (candles['sma50'].shift(1) >= candles['sma200'].shift(1))
    
    # Print crossover points
    crossover_points = candles[candles['crossover']]
    print(f"Found {len(crossover_points)} bullish crossovers")
    for idx, row in crossover_points.iterrows():
        print(f"Bullish crossover on {row['time'].strftime('%Y-%m-%d')}: Price = {row['close']}")
        
except Exception as e:
    print(f"Error: {e}")
finally:
    client.disconnect()
```

---

*This documentation was last updated on April 11, 2025.*
