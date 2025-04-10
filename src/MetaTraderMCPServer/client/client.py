"""
MetaTrader 5 client main module.

This module provides a unified interface for all MT5 operations.
"""
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime

from .connection import MT5Connection
from .account import MT5Account
from .market import MT5Market
from .orders import MT5Orders, OrderType, OrderFilling, OrderTime, TradeAction
from .history import MT5History, DealType, OrderState
from .exceptions import MT5ClientError


class MT5Client:
    """
    Main client class for MetaTrader 5 operations.
    
    Provides a unified interface for all MT5 operations including
    connection management, account information, market data,
    order execution, and history retrieval.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the MT5 client.
        
        Args:
            config: Optional configuration dictionary with connection parameters.
                   Can include: path, login, password, server, timeout, portable
        """
        self._config = config or {}
        self._connection = MT5Connection(config)
        self._account = MT5Account(self._connection)
        self.market = MT5Market(self._connection)
        self._orders = MT5Orders(self._connection)
        self._history = MT5History(self._connection)
    
    # Connection methods
    
    def connect(self) -> bool:
        """
        Connect to the MetaTrader 5 terminal.
        
        If login credentials are provided in config, also performs login.
        Terminal is automatically launched if needed.
        
        Returns:
            bool: True if connection was successful.
            
        Raises:
            ConnectionError: If connection fails with specific error details.
        """
        return self._connection.connect()
    
    def disconnect(self) -> bool:
        """
        Disconnect from the MetaTrader 5 terminal.
        
        Properly shuts down the connection to release resources.
        
        Returns:
            bool: True if disconnection was successful.
        """
        return self._connection.disconnect()
    
    def is_connected(self) -> bool:
        """
        Check if connected to the MetaTrader 5 terminal.
        
        Returns:
            bool: True if connected.
        """
        return self._connection.is_connected()
    
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
        return self._connection.get_terminal_info()
    
    def get_version(self) -> Tuple[int, int, int, int]:
        """
        Get the version of the connected MetaTrader 5 terminal.
        
        Returns:
            Tuple[int, int, int, int]: Version as (major, minor, build, revision).
            
        Raises:
            ConnectionError: If not connected to terminal.
        """
        return self._connection.get_version()
    
    def last_error(self) -> Tuple[int, str]:
        """
        Get the last error code and description.
        
        Returns:
            Tuple[int, str]: Error code and description.
        """
        return self._connection.last_error()
    
    # Account methods
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get comprehensive account information.
        
        Returns a dictionary with all account properties including balance,
        equity, margin, leverage, etc.
        
        Returns:
            Dict[str, Any]: Account information.
            
        Raises:
            AccountError: If account information cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        return self._account.get_account_info()
    
    def get_balance(self) -> float:
        """
        Get current account balance.
        
        Balance is the amount of money in the account without considering
        open positions.
        
        Returns:
            float: Current account balance.
            
        Raises:
            AccountError: If balance cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        return self._account.get_balance()
    
    def get_equity(self) -> float:
        """
        Get current account equity.
        
        Equity is the balance plus floating profit/loss from open positions.
        
        Returns:
            float: Current account equity.
            
        Raises:
            AccountError: If equity cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        return self._account.get_equity()
    
    def get_margin(self) -> float:
        """
        Get current used margin.
        
        Margin is the amount of money reserved as a deposit to maintain
        open positions.
        
        Returns:
            float: Current used margin.
            
        Raises:
            AccountError: If margin cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        return self._account.get_margin()
    
    def get_free_margin(self) -> float:
        """
        Get current free margin.
        
        Free margin is the amount of money available for opening new positions.
        
        Returns:
            float: Current free margin.
            
        Raises:
            AccountError: If free margin cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        return self._account.get_free_margin()
    
    def get_margin_level(self) -> float:
        """
        Get current margin level.
        
        Margin level is calculated as (Equity / Margin) * 100%.
        
        Returns:
            float: Current margin level in percentage.
            
        Raises:
            AccountError: If margin level cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        return self._account.get_margin_level()
    
    # Market methods
    
    def get_symbols(self, group: Optional[str] = None) -> List[str]:
        """
        Get list of all available market symbols.
        
        Args:
            group: Filter symbols by group pattern, e.g., "*USD*" for USD pairs.
                  Wildcards can be used.
        
        Returns:
            List[str]: List of symbol names.
            
        Raises:
            MarketError: If symbols cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        return self._market.get_symbols(group)
    
    
    # def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
    #     """
    #     Get detailed information about a specific symbol.
        
    #     Returns a dictionary with symbol properties including point value,
    #     digits, contract size, etc.
        
    #     Args:
    #         symbol: Symbol name.
            
    #     Returns:
    #         Dict[str, Any]: Symbol information.
            
    #     Raises:
    #         MarketError: If symbol information cannot be retrieved.
    #         ConnectionError: If not connected to terminal.
    #     """
    #     return self._market.get_symbol_info(symbol)
    
    # def get_symbol_price(self, symbol: str) -> Dict[str, float]:
    #     """
    #     Get current price for a symbol.
        
    #     Args:
    #         symbol: Symbol name.
            
    #     Returns:
    #         Dict[str, float]: Dictionary with price information (bid, ask, last, etc.).
            
    #     Raises:
    #         MarketError: If prices cannot be retrieved.
    #         ConnectionError: If not connected to terminal.
    #     """
    #     return self._market.get_symbol_price(symbol)
    
    # def get_candles(
    #     self, 
    #     symbol: str, 
    #     timeframe: Union[TimeFrame, str, int], 
    #     from_date: Optional[datetime] = None,
    #     to_date: Optional[datetime] = None,
    #     count: Optional[int] = None
    # ) -> List[Dict[str, Any]]:
    #     """
    #     Get historical price data (OHLCV) for a symbol.
        
    #     Args:
    #         symbol: Symbol name.
    #         timeframe: Timeframe (can be TimeFrame enum, string like "M1", or integer).
    #         from_date: Start date for historical data (optional).
    #         to_date: End date for historical data (optional).
    #         count: Maximum number of candles to retrieve (optional).
            
    #     Returns:
    #         List[Dict[str, Any]]: List of candles with OHLCV data.
            
    #     Raises:
    #         MarketError: If historical data cannot be retrieved.
    #         ConnectionError: If not connected to terminal.
    #     """
    #     return self._market.get_candles(symbol, timeframe, from_date, to_date, count)
    
    # def get_ticks(
    #     self,
    #     symbol: str,
    #     from_date: datetime,
    #     to_date: Optional[datetime] = None,
    #     count: Optional[int] = None,
    #     mode: CopyTicksMode = CopyTicksMode.ALL
    # ) -> List[Dict[str, Any]]:
    #     """
    #     Get tick data for a symbol.
        
    #     Args:
    #         symbol: Symbol name.
    #         from_date: Start date for tick data.
    #         to_date: End date for tick data (optional).
    #         count: Maximum number of ticks to retrieve (optional).
    #         mode: Type of ticks to retrieve (default: ALL).
            
    #     Returns:
    #         List[Dict[str, Any]]: List of ticks with price data.
            
    #     Raises:
    #         MarketError: If tick data cannot be retrieved.
    #         ConnectionError: If not connected to terminal.
    #     """
    #     return self._market.get_ticks(symbol, from_date, to_date, count, mode)
    
    # def select_symbol(self, symbol: str, enable: bool = True) -> bool:
    #     """
    #     Add or remove a symbol from the Market Watch window.
        
    #     Args:
    #         symbol: Symbol name.
    #         enable: True to add, False to remove.
            
    #     Returns:
    #         bool: True if operation was successful.
            
    #     Raises:
    #         MarketError: If symbol selection fails.
    #         ConnectionError: If not connected to terminal.
    #     """
    #     return self._market.select_symbol(symbol, enable)
    
    # # Order methods
    
    # def execute_trade(
    #     self, 
    #     symbol: str, 
    #     order_type: Union[OrderType, str], 
    #     volume: float, 
    #     price: Optional[float] = None,
    #     stop_loss: Optional[float] = None,
    #     take_profit: Optional[float] = None,
    #     deviation: Optional[int] = None,
    #     magic: Optional[int] = None,
    #     comment: Optional[str] = None,
    #     type_filling: Optional[OrderFilling] = None,
    #     type_time: Optional[OrderTime] = None,
    #     expiration: Optional[datetime] = None
    # ) -> Dict[str, Any]:
    #     """
    #     Execute a trade order.
        
    #     Args:
    #         symbol: Symbol name.
    #         order_type: Type of order (can be OrderType enum or string).
    #         volume: Trade volume in lots.
    #         price: Price for pending orders (optional).
    #         stop_loss: Stop loss level (optional).
    #         take_profit: Take profit level (optional).
    #         deviation: Maximum price deviation in points (optional).
    #         magic: Expert Advisor ID (optional).
    #         comment: Order comment (optional).
    #         type_filling: Order filling type (optional).
    #         type_time: Order lifetime type (optional).
    #         expiration: Order expiration time (optional).
            
    #     Returns:
    #         Dict[str, Any]: Order result information.
            
    #     Raises:
    #         OrderError: If order execution fails.
    #         ConnectionError: If not connected to terminal.
    #     """
    #     # Convert string order type to enum if needed
    #     if isinstance(order_type, str):
    #         order_type = OrderType[order_type.upper()]
            
    #     return self._orders.execute_trade(
    #         symbol, order_type, volume, price, stop_loss, take_profit, 
    #         deviation, magic, comment, type_filling, type_time, expiration
    #     )
    
    # def modify_order(
    #     self,
    #     ticket: int,
    #     price: Optional[float] = None,
    #     stop_loss: Optional[float] = None,
    #     take_profit: Optional[float] = None,
    #     type_time: Optional[OrderTime] = None,
    #     expiration: Optional[datetime] = None
    # ) -> bool:
    #     """
    #     Modify an existing pending order.
        
    #     Args:
    #         ticket: Order ticket number.
    #         price: New price for pending orders (optional).
    #         stop_loss: New stop loss level (optional).
    #         take_profit: New take profit level (optional).
    #         type_time: New order lifetime type (optional).
    #         expiration: New order expiration time (optional).
            
    #     Returns:
    #         bool: True if modification was successful.
            
    #     Raises:
    #         OrderError: If order modification fails.
    #         ConnectionError: If not connected to terminal.
    #     """
    #     return self._orders.modify_order(ticket, price, stop_loss, take_profit, type_time, expiration)
    
    # def modify_position(
    #     self,
    #     ticket: int,
    #     stop_loss: Optional[float] = None,
    #     take_profit: Optional[float] = None
    # ) -> bool:
    #     """
    #     Modify stop loss and take profit for an open position.
        
    #     Args:
    #         ticket: Position ticket number.
    #         stop_loss: New stop loss level (optional).
    #         take_profit: New take profit level (optional).
            
    #     Returns:
    #         bool: True if modification was successful.
            
    #     Raises:
    #         OrderError: If position modification fails.
    #         ConnectionError: If not connected to terminal.
    #     """
    #     return self._orders.modify_position(ticket, stop_loss, take_profit)
    
    # def close_position(
    #     self,
    #     ticket: int,
    #     volume: Optional[float] = None
    # ) -> bool:
    #     """
    #     Close an existing position.
        
    #     Args:
    #         ticket: Position ticket number.
    #         volume: Volume to close (partial close if less than position volume).
            
    #     Returns:
    #         bool: True if close operation was successful.
            
    #     Raises:
    #         OrderError: If position closing fails.
    #         ConnectionError: If not connected to terminal.
    #     """
    #     return self._orders.close_position(ticket, volume)
    
    # def delete_order(
    #     self,
    #     ticket: int
    # ) -> bool:
    #     """
    #     Delete a pending order.
        
    #     Args:
    #         ticket: Order ticket number.
            
    #     Returns:
    #         bool: True if deletion was successful.
            
    #     Raises:
    #         OrderError: If order deletion fails.
    #         ConnectionError: If not connected to terminal.
    #     """
    #     return self._orders.delete_order(ticket)
    
    # def get_orders(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
    #     """
    #     Get list of all active pending orders.
        
    #     Args:
    #         symbol: Filter orders by symbol (optional).
            
    #     Returns:
    #         List[Dict[str, Any]]: List of pending orders.
            
    #     Raises:
    #         OrderError: If orders cannot be retrieved.
    #         ConnectionError: If not connected to terminal.
    #     """
    #     return self._orders.get_orders(symbol)
    
    # def get_positions(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
    #     """
    #     Get list of all open positions.
        
    #     Args:
    #         symbol: Filter positions by symbol (optional).
            
    #     Returns:
    #         List[Dict[str, Any]]: List of open positions.
            
    #     Raises:
    #         OrderError: If positions cannot be retrieved.
    #         ConnectionError: If not connected to terminal.
    #     """
    #     return self._orders.get_positions(symbol)
    
    # History methods
    
    def get_deals(
        self,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        group: Optional[str] = None,
        ticket: Optional[int] = None,
        position: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get historical deals.
        
        Args:
            from_date: Start date for history (optional).
            to_date: End date for history (optional).
            group: Filter by group pattern, e.g., "*USD*" (optional).
            ticket: Filter by specific deal ticket (optional).
            position: Filter by position identifier (optional).
            
        Returns:
            List[Dict[str, Any]]: List of historical deals.
            
        Raises:
            HistoryError: If deals cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        return self._history.get_deals(from_date, to_date, group, ticket, position)
    
    def get_history_orders(
        self,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        group: Optional[str] = None,
        ticket: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get historical orders.
        
        Args:
            from_date: Start date for history (optional).
            to_date: End date for history (optional).
            group: Filter by group pattern, e.g., "*USD*" (optional).
            ticket: Filter by specific order ticket (optional).
            
        Returns:
            List[Dict[str, Any]]: List of historical orders.
            
        Raises:
            HistoryError: If orders cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        return self._history.get_orders(from_date, to_date, group, ticket)
    
    def get_statistics(
        self,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        group: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get trading statistics.
        
        Args:
            from_date: Start date for statistics (optional).
            to_date: End date for statistics (optional).
            group: Filter by symbol group pattern (optional).
            
        Returns:
            Dict[str, Any]: Trading statistics.
            
        Raises:
            HistoryError: If statistics cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        return self._history.get_statistics(from_date, to_date, group)
    
    # Calculation methods
    
    def calculate_margin(
        self,
        symbol: str,
        order_type: Union[OrderType, str],
        volume: float,
        price: float
    ) -> float:
        """
        Calculate margin required for a trade.
        
        Args:
            symbol: Symbol name.
            order_type: Type of order (can be OrderType enum or string).
            volume: Trade volume in lots.
            price: Order price.
            
        Returns:
            float: Required margin amount.
            
        Raises:
            OrderError: If margin calculation fails.
            ConnectionError: If not connected to terminal.
        """
        # Convert string order type to enum if needed
        if isinstance(order_type, str):
            order_type = OrderType[order_type.upper()]
            
        return self._orders.calculate_margin(symbol, order_type, volume, price)
    
    def calculate_profit(
        self,
        symbol: str,
        order_type: Union[OrderType, str],
        volume: float,
        price_open: float,
        price_close: float
    ) -> float:
        """
        Calculate profit for a trade.
        
        Args:
            symbol: Symbol name.
            order_type: Type of order (can be OrderType enum or string).
            volume: Trade volume in lots.
            price_open: Opening price.
            price_close: Closing price.
            
        Returns:
            float: Expected profit amount.
            
        Raises:
            OrderError: If profit calculation fails.
            ConnectionError: If not connected to terminal.
        """
        # Convert string order type to enum if needed
        if isinstance(order_type, str):
            order_type = OrderType[order_type.upper()]
            
        return self._orders.calculate_profit(symbol, order_type, volume, price_open, price_close)
