# MT5 History Module Documentation 📊

## Overview 🌟

The `history` module provides comprehensive functionality for retrieving and analyzing historical trading data from MetaTrader 5. It enables you to access historical deals, orders, and convert them to pandas DataFrames for further analysis. This module is built on top of the connection module and offers a robust, error-handled interface to MT5's historical data functions.

## Quick Start Guide 🚀

```python
from metatrader_client.connection import MT5Connection
from metatrader_client.history import MT5History
from datetime import datetime, timedelta

# Set up configuration
config = {
    "login": 12345678,  # Your MT5 account number
    "password": "your-password",
    "server": "Your-Broker-Server",
    "debug": True  # Enable debug logging
}

# Create connection and history objects
connection = MT5Connection(config)
history = MT5History(connection)

try:
    # Connect to terminal
    connection.connect()
    print("✅ Connected to MetaTrader 5!")
    
    # Define time range for history queries
    to_date = datetime.now()
    from_date = to_date - timedelta(days=30)  # Last 30 days
    
    # Get total counts
    total_deals = history.get_total_deals(from_date, to_date)
    total_orders = history.get_total_orders(from_date, to_date)
    print(f"Found {total_deals} deals and {total_orders} orders in the last 30 days")
    
    # Retrieve deals history
    deals = history.get_deals(from_date, to_date)
    print(f"Retrieved {len(deals)} deals")
    
    # Filter orders by symbol group
    usd_orders = history.get_orders(from_date, to_date, group="*USD*")
    print(f"Retrieved {len(usd_orders)} USD-related orders")
    
    # Get specific deal or order by ticket
    if deals:
        ticket = deals[0]["ticket"]
        specific_deal = history.get_deals(ticket=ticket)
        print(f"Retrieved deal with ticket {ticket}")
    
    # Convert to pandas DataFrame for analysis
    deals_df = history.get_deals_as_dataframe(from_date, to_date)
    orders_df = history.get_orders_as_dataframe(from_date, to_date)
    
    print(f"Deals DataFrame shape: {deals_df.shape}")
    print(f"Orders DataFrame shape: {orders_df.shape}")
    
    # Disconnect when done
    connection.disconnect()
    print("✅ Disconnected from MetaTrader 5")
    
except Exception as e:
    print(f"❌ Error: {e}")
```

## Detailed Documentation 📖

### History Class Structure 🏗️

The `MT5History` class is the main component of this module and provides the following structure:

#### Constructor

```python
MT5History(connection: MT5Connection)
```

Creates a new history manager using an existing connection to the MT5 terminal.

**Parameters:**
- `connection`: An instance of MT5Connection that is used to communicate with the terminal

### Key Methods 🔑

#### Deal History

##### `get_deals()` 📝
```python
get_deals(
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    group: Optional[str] = None,
    ticket: Optional[int] = None,
    position: Optional[int] = None
) -> List[Dict[str, Any]]
```

Retrieves historical deals matching the specified criteria.

**Parameters:**
- `from_date`: Start date for history (optional, defaults to 30 days ago)
- `to_date`: End date for history (optional, defaults to current time)
- `group`: Filter by group pattern, e.g., "*USD*" (optional)
- `ticket`: Filter by specific deal ticket (optional)
- `position`: Filter by position identifier (optional)

**Returns:**
- `List[Dict[str, Any]]`: List of historical deals with properties including ticket, time, type, symbol, volume, price, profit, etc.

**Raises:**
- `DealsHistoryError`: If deals cannot be retrieved
- `ConnectionError`: If not connected to terminal

**Notes:**
- If `ticket` or `position` is specified, it takes priority over date range filters
- Date parameters are required for general history retrieval and have default values if not provided

##### `get_total_deals()` 🔢
```python
get_total_deals(
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None
) -> int
```

Gets the total number of deals in history within the specified date range.

**Parameters:**
- `from_date`: Start date for history (optional, defaults to 30 days ago)
- `to_date`: End date for history (optional, defaults to current time)

**Returns:**
- `int`: Number of deals in the specified date range

**Raises:**
- `DealsHistoryError`: If deals count cannot be retrieved
- `ConnectionError`: If not connected to terminal

#### Order History

##### `get_orders()` 📋
```python
get_orders(
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    group: Optional[str] = None,
    ticket: Optional[int] = None
) -> List[Dict[str, Any]]
```

Retrieves historical orders matching the specified criteria.

**Parameters:**
- `from_date`: Start date for history (optional, defaults to 30 days ago)
- `to_date`: End date for history (optional, defaults to current time)
- `group`: Filter by group pattern, e.g., "*USD*" (optional)
- `ticket`: Filter by specific order ticket (optional)

**Returns:**
- `List[Dict[str, Any]]`: List of historical orders with properties including ticket, time_setup, time_done, type, state, symbol, volume, etc.

**Raises:**
- `OrdersHistoryError`: If orders cannot be retrieved
- `ConnectionError`: If not connected to terminal

**Notes:**
- If `ticket` is specified, it takes priority over date range filters
- Date parameters are required for general history retrieval and have default values if not provided

##### `get_total_orders()` 🔢
```python
get_total_orders(
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None
) -> int
```

Gets the total number of orders in history within the specified date range.

**Parameters:**
- `from_date`: Start date for history (optional, defaults to 30 days ago)
- `to_date`: End date for history (optional, defaults to current time)

**Returns:**
- `int`: Number of orders in the specified date range

**Raises:**
- `OrdersHistoryError`: If orders count cannot be retrieved
- `ConnectionError`: If not connected to terminal

#### DataFrame Integration

##### `get_deals_as_dataframe()` 📊
```python
get_deals_as_dataframe(
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    group: Optional[str] = None,
    ticket: Optional[int] = None,
    position: Optional[int] = None
) -> pd.DataFrame
```

Retrieves historical deals and converts them to a pandas DataFrame.

**Parameters:**
- `from_date`: Start date for history (optional, defaults to 30 days ago)
- `to_date`: End date for history (optional, defaults to current time)
- `group`: Filter by group pattern, e.g., "*USD*" (optional)
- `ticket`: Filter by specific deal ticket (optional)
- `position`: Filter by position identifier (optional)

**Returns:**
- `pd.DataFrame`: DataFrame of historical deals with time as index

**Raises:**
- `DealsHistoryError`: If deals cannot be retrieved or DataFrame creation fails
- `ConnectionError`: If not connected to terminal

**Notes:**
- The time column is converted to datetime and set as the DataFrame index
- Returns an empty DataFrame if no deals match the criteria

##### `get_orders_as_dataframe()` 📊
```python
get_orders_as_dataframe(
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    group: Optional[str] = None,
    ticket: Optional[int] = None
) -> pd.DataFrame
```

Retrieves historical orders and converts them to a pandas DataFrame.

**Parameters:**
- `from_date`: Start date for history (optional, defaults to 30 days ago)
- `to_date`: End date for history (optional, defaults to current time)
- `group`: Filter by group pattern, e.g., "*USD*" (optional)
- `ticket`: Filter by specific order ticket (optional)

**Returns:**
- `pd.DataFrame`: DataFrame of historical orders with time_setup as index

**Raises:**
- `OrdersHistoryError`: If orders cannot be retrieved or DataFrame creation fails
- `ConnectionError`: If not connected to terminal

**Notes:**
- The time_setup, time_done, and time_expiration columns are converted to datetime
- time_setup is set as the DataFrame index
- Returns an empty DataFrame if no orders match the criteria

### Enumerations 📝

The module includes two enumeration classes to help work with deals and orders:

#### DealType
Represents the types of deals in MetaTrader 5.

| Name | Value | Description |
|------|-------|-------------|
| BUY | 0 | Buy |
| SELL | 1 | Sell |
| BALANCE | 2 | Balance |
| CREDIT | 3 | Credit |
| CHARGE | 4 | Charge |
| CORRECTION | 5 | Correction |
| BONUS | 6 | Bonus |
| COMMISSION | 7 | Commission |
| COMMISSION_DAILY | 8 | Daily commission |
| COMMISSION_MONTHLY | 9 | Monthly commission |
| AGENT_COMMISSION | 10 | Agent commission |
| INTEREST | 11 | Interest |
| CANCELED_BUY | 12 | Canceled buy deal |
| CANCELED_SELL | 13 | Canceled sell deal |

#### OrderState
Represents the states of orders in MetaTrader 5.

| Name | Value | Description |
|------|-------|-------------|
| STARTED | 0 | Order started |
| PLACED | 1 | Order placed |
| CANCELED | 2 | Order canceled |
| PARTIAL | 3 | Order partially executed |
| FILLED | 4 | Order filled |
| REJECTED | 5 | Order rejected |
| EXPIRED | 6 | Order expired |
| REQUEST_ADD | 7 | Order requested to add |
| REQUEST_MODIFY | 8 | Order requested to modify |
| REQUEST_CANCEL | 9 | Order requested to cancel |

## Error Handling ⚠️

The History module defines specific exception classes for error handling:

- `HistoryError`: Base exception for all history-related errors
- `DealsHistoryError`: Raised when deals history operations fail
- `OrdersHistoryError`: Raised when orders history operations fail
- `StatisticsError`: Raised when statistics operations fail
- `ConnectionError`: Raised when not connected to the MT5 terminal

All exceptions include an error message and an error code from MT5 when available.

## Best Practices 💡

1. **Check connection status first** - Always verify the connection before history operations
   ```python
   if connection.is_connected():
       deals = history.get_deals()
   ```

2. **Use try/except blocks** - Handle exceptions properly for robust error handling
   ```python
   try:
       deals = history.get_deals(from_date, to_date)
   except DealsHistoryError as e:
       print(f"Error retrieving deals: {e}")
   ```

3. **Specify date ranges explicitly** - For performance and clarity, provide from_date and to_date
   ```python
   # Better than relying on defaults
   from_date = datetime.now() - timedelta(days=7)  # Last week
   to_date = datetime.now()
   deals = history.get_deals(from_date, to_date)
   ```

4. **Filter data efficiently** - Use group, ticket, or position parameters for focused queries
   ```python
   # More efficient than retrieving all deals then filtering in Python
   eurusd_deals = history.get_deals(from_date, to_date, group="*EURUSD*")
   ```

5. **Use pandas for analysis** - Leverage the DataFrame integration for data analysis
   ```python
   deals_df = history.get_deals_as_dataframe(from_date, to_date)
   # Calculate daily profit
   daily_profit = deals_df.groupby(deals_df.index.date)["profit"].sum()
   ```

## Testing 🧪

The History module includes comprehensive unit and integration tests:

- **Unit tests**: Test the module functionality with mocked MT5 responses
- **Integration tests**: Test with real MT5 connection
- **Parameter passing tests**: Validate the correct passing of parameters to MT5 API

To run history tests:

```bash
python -m tests.run_tests history
```

## Troubleshooting 🔍

### Common Issues

1. **No deals/orders returned**
   - Check date range parameters
   - Verify the account has trading history
   - Ensure the group filter pattern is correct

2. **Connection errors**
   - Ensure MT5 terminal is running
   - Check login credentials
   - Verify network connectivity

3. **Permission errors**
   - Check MT5 terminal permissions
   - Verify account access rights

### Getting Help

If you encounter issues:
1. Check the error message and code
2. View the logs (with debug=True)
3. Check the MT5 documentation for specific error codes

## API Reference 📚

### Classes

- `MT5History`: Primary class for history operations
- `DealType`: Enumeration of deal types
- `OrderState`: Enumeration of order states

### Exception Classes

- `HistoryError`: Base exception class
- `DealsHistoryError`: Deals-specific errors
- `OrdersHistoryError`: Orders-specific errors
- `StatisticsError`: Statistics-specific errors
- `ConnectionError`: Connection-related errors

## Related Modules 🔄

- **Connection Module**: Required for establishing connection to MT5
- **Account Module**: Provides account information to correlate with historical data

## Version History 📅

- **1.0.0**: Initial release with deals and orders history retrieval
- **1.0.1**: Added DataFrame integration
