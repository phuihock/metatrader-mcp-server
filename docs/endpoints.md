# API Endpoints

## Accounts

- **GET** `/api/v1/accounts/info`  
  Retrieve account statistics (balance, equity, profit).

## History

- **GET** `/api/v1/history/deals?from_date=&to_date=&symbol=`  
  Get historical deals.
- **GET** `/api/v1/history/orders?from_date=&to_date=&symbol=`  
  Get historical orders.

## Market

- **GET** `/api/v1/market/candles/latest?symbol_name=&timeframe=&count=`  
  Fetch latest candle data.
- **GET** `/api/v1/market/price/{symbol_name}`  
  Get current price for a symbol.
- **GET** `/api/v1/market/symbols`  
  List all symbols.
- **GET** `/api/v1/market/symbols/filter?group=`  
  Filter symbols by group pattern.

## Orders

### Pending Orders

- **GET** `/api/v1/orders/pending`  
  List all pending orders.
- **GET** `/api/v1/orders/pending/symbol/{symbol}`  
  Pending orders for a symbol.
- **GET** `/api/v1/orders/pending/{id}`  
  Pending order by ID.
- **PUT** `/api/v1/orders/pending/{id}`  
  Modify a pending order.
- **DELETE** `/api/v1/orders/pending/{id}`  
  Cancel a pending order by ID.
- **DELETE** `/api/v1/orders/pending`  
  Cancel all pending orders.
- **DELETE** `/api/v1/orders/pending/symbol/{symbol}`  
  Cancel pending orders for a symbol.

### New Order Placement

- **POST** `/api/v1/orders/market`  
  Place a market order.
- **POST** `/api/v1/orders/pending`  
  Place a pending order.

## Positions

- **GET** `/api/v1/positions`  
  List all open positions.
- **GET** `/api/v1/positions/symbol/{symbol}`  
  Open positions for a symbol.
- **GET** `/api/v1/positions/{id}`  
  Open position by ID.
- **PUT** `/api/v1/positions/{id}`  
  Modify an open position.
- **DELETE** `/api/v1/positions/{id}`  
  Close a position by ID.
- **DELETE** `/api/v1/positions`  
  Close all positions.
- **DELETE** `/api/v1/positions/symbol/{symbol}`  
  Close positions for a symbol.
- **DELETE** `/api/v1/positions/profitable`  
  Close all profitable positions.
- **DELETE** `/api/v1/positions/losing`  
  Close all losing positions.
