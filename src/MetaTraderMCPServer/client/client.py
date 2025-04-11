"""
MetaTrader 5 client main module.

This module provides a unified interface for all MT5 operations.
"""
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime

from .connection import MT5Connection
from .account import MT5Account
from .market import MT5Market
from .orders import MT5Orders
from .history import MT5History
from .types import OrderType

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
        self.orders = MT5Orders(self._connection)
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
