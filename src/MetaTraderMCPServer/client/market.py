"""
MetaTrader 5 market operations module.

This module handles market data retrieval and symbol information.
"""
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime
from enum import Enum
from .exceptions import MarketError


class TimeFrame(Enum):
    """Timeframes supported by MetaTrader 5."""
    M1 = 1      # 1 minute
    M2 = 2      # 2 minutes
    M3 = 3      # 3 minutes
    M4 = 4      # 4 minutes
    M5 = 5      # 5 minutes
    M6 = 6      # 6 minutes
    M10 = 10    # 10 minutes
    M12 = 12    # 12 minutes
    M15 = 15    # 15 minutes
    M20 = 20    # 20 minutes
    M30 = 30    # 30 minutes
    H1 = 60     # 1 hour
    H2 = 120    # 2 hours
    H3 = 180    # 3 hours
    H4 = 240    # 4 hours
    H6 = 360    # 6 hours
    H8 = 480    # 8 hours
    H12 = 720   # 12 hours
    D1 = 1440   # 1 day
    W1 = 10080  # 1 week
    MN1 = 43200 # 1 month


class CopyTicksMode(Enum):
    """Tick copy modes for MetaTrader 5."""
    ALL = 0     # All ticks
    INFO = 1    # Info ticks only (non-empty price changes)
    TRADES = 2  # Trade ticks only


class MT5Market:
    """
    Handles MetaTrader 5 market operations.
    
    Provides methods to retrieve market data, symbol information, and prices.
    """
    
    def __init__(self, connection):
        """
        Initialize the market operations handler.
        
        Args:
            connection: MT5Connection instance for terminal communication.
        """
        self._connection = connection
    
    def get_symbols(self, group: Optional[str] = None) -> List[str]:
        """
        Get list of all available market symbols.
        
        Args:
            group: Filter symbols by group pattern (e.g., "*USD*" for USD pairs).
                  Wildcards can be used.
        
        Returns:
            List[str]: List of symbol names.
            
        Raises:
            MarketError: If symbols cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        pass
    
    def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific symbol.
        
        Returns a dictionary with symbol properties including:
        - name: Symbol name
        - description: Symbol description
        - path: Symbol path in the symbol tree
        - point: Point value (smallest price change)
        - digits: Number of digits after decimal point
        - trade_calc_mode: Contract price calculation mode
        - trade_mode: Order execution type
        - spread: Current spread in points
        - spread_float: Whether spread is floating
        - tick_size: Minimal price change
        - contract_size: Contract size
        - volume_min: Minimal volume for a deal
        - volume_max: Maximal volume for a deal
        - volume_step: Minimal volume change step
        - swap_mode: Swap calculation mode
        - swap_long: Long swap value
        - swap_short: Short swap value
        
        Args:
            symbol: Symbol name.
            
        Returns:
            Dict[str, Any]: Symbol information.
            
        Raises:
            MarketError: If symbol information cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        pass
    
    def get_symbol_price(self, symbol: str) -> Dict[str, float]:
        """
        Get current price for a symbol.
        
        Args:
            symbol: Symbol name.
            
        Returns:
            Dict[str, float]: Dictionary with price information:
                - bid: Bid price
                - ask: Ask price
                - last: Last deal price
                - volume: Volume for the current last price
                - time: Time of the last price update
            
        Raises:
            MarketError: If prices cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        pass
    
    def get_candles(
        self, 
        symbol: str, 
        timeframe: Union[TimeFrame, str, int], 
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        count: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get historical price data (OHLCV) for a symbol.
        
        Args:
            symbol: Symbol name.
            timeframe: Timeframe (can be TimeFrame enum, string like "M1", or integer).
            from_date: Start date for historical data (optional).
            to_date: End date for historical data (optional).
            count: Maximum number of candles to retrieve (optional).
            
        Returns:
            List[Dict[str, Any]]: List of candles with OHLCV data:
                - time: Candle time
                - open: Open price
                - high: High price
                - low: Low price
                - close: Close price
                - tick_volume: Tick volume
                - spread: Spread
                - real_volume: Real volume (if available)
            
        Raises:
            MarketError: If historical data cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        pass
    
    def get_ticks(
        self,
        symbol: str,
        from_date: datetime,
        to_date: Optional[datetime] = None,
        count: Optional[int] = None,
        mode: CopyTicksMode = CopyTicksMode.ALL
    ) -> List[Dict[str, Any]]:
        """
        Get tick data for a symbol.
        
        Args:
            symbol: Symbol name.
            from_date: Start date for tick data.
            to_date: End date for tick data (optional).
            count: Maximum number of ticks to retrieve (optional).
            mode: Type of ticks to retrieve (default: ALL).
            
        Returns:
            List[Dict[str, Any]]: List of ticks with price data:
                - time: Tick time in milliseconds
                - bid: Bid price
                - ask: Ask price
                - last: Last deal price
                - volume: Volume for the current last price
                - flags: Tick flags
            
        Raises:
            MarketError: If tick data cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        pass
    
    def get_market_depth(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Get market depth (DOM) for a symbol.
        
        Args:
            symbol: Symbol name.
            
        Returns:
            List[Dict[str, Any]]: List of market depth entries:
                - type: Entry type (0-sell, 1-buy)
                - price: Price
                - volume: Volume
                - time: Time
            
        Raises:
            MarketError: If market depth cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        pass
    
    def select_symbol(self, symbol: str, enable: bool = True) -> bool:
        """
        Add or remove a symbol from the Market Watch window.
        
        Args:
            symbol: Symbol name.
            enable: True to add, False to remove.
            
        Returns:
            bool: True if operation was successful.
            
        Raises:
            MarketError: If symbol selection fails.
            ConnectionError: If not connected to terminal.
        """
        pass
