"""
MetaTrader 5 market operations module.

This module provides a comprehensive interface for interacting with MetaTrader 5 market data.
It handles various market operations including:
- Symbol information retrieval
- Price data access
- Historical candle data fetching

The MT5Market class serves as the main entry point for all market-related operations.
"""
# Standard library imports
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

# Third-party imports
import MetaTrader5 as mt5
import pandas as pd

# Local application imports
from .types import Timeframe
from .exceptions import SymbolNotFoundError, InvalidTimeframeError, MarketDataError


class MT5Market:
    """
    Handles MetaTrader 5 market operations.
    
    Provides methods to retrieve market data, symbol information, and prices.
    This class requires an active MT5 connection to function properly.
    """
    
    def __init__(self, connection):
        """
        Initialize the market operations handler.
        
        Establishes a link to the MetaTrader 5 terminal through the provided connection
        object. This connection must be active and properly initialized before
        using any methods of this class.
        
        Args:
            connection: MT5Connection instance for terminal communication.
                        This object handles the underlying connection to the MT5 terminal.
        """
        self._connection = connection
    
    def get_symbols(self, group: Optional[str] = None) -> List[str]:
        """
        Get list of all available market symbols.
        
        Retrieves a list of all symbols available in the Market Watch or filtered by
        a specific pattern. This is useful for discovering tradable instruments or
        verifying if a specific symbol exists.
        
        Args:
            group: Filter symbols by group pattern (e.g., "*USD*" for USD pairs).
                  Wildcards can be used. If None, returns all symbols.
                  Examples:
                  - "*" - all symbols
                  - "EUR*" - all symbols starting with EUR
                  - "*USD*" - all symbols containing USD
                  - "EUR*,GBP*" - all symbols starting with EUR or GBP
        
        Returns:
            List[str]: List of symbol names matching the filter criteria.
            
        Raises:
            MarketError: If symbols cannot be retrieved due to API errors.
            ConnectionError: If not connected to terminal or connection is lost.
        
        Example:
            >>> market = MT5Market(connection)
            >>> forex_pairs = market.get_symbols("*USD*")
            >>> print(forex_pairs)
            ['EURUSD', 'GBPUSD', 'USDJPY', ...]
        """
        symbols = []
        names = []

        # Get symbols based on filter or get all symbols
        if (group == None):
            symbols = mt5.symbols_get()
        else:
            symbols = mt5.symbols_get(group)
        
        # Extract symbol names from symbol objects
        if (len(symbols) > 0):
            for symbol in symbols:
                names.append(symbol.name)
        
        return names

    def get_symbol_info(self, symbol_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific symbol.
        
        Retrieves comprehensive information about a trading symbol including
        price data, trading parameters, and market specifications. This method
        provides all the technical details needed for symbol analysis and trading.
        
        Args:
            symbol_name: Symbol name (e.g., "EURUSD", "XAUUSD").
                         Must be an exact match to an existing symbol.
            
        Returns:
            Dict[str, Any]: Dictionary with symbol information, including:
            - name (str): Symbol name (e.g., EURUSD).
            - description (str): Description of the symbol.
            - currency_base (str): Base currency of the symbol.
            - currency_profit (str): Profit currency of the symbol.
            - bid (float): Current Bid price.
            - ask (float): Current Ask price.
            - spread (int): Spread value in points.
            - spread_float (bool): Indicates if the spread is floating.
            - point (float): Point size in the quote currency.
            - digits (int): Number of decimal places in the symbol's price.
            - trade_contract_size (float): Contract size per lot.
            - volume_min (float): Minimum trade volume.
            - volume_max (float): Maximum trade volume.
            - volume_step (float): Step size for trade volume.
            - trade_tick_value (float): Value of one tick movement in deposit currency.
            - trade_tick_size (float): Tick size in points.
            - trade_mode (int): Order execution type.
            - trade_exemode (int): Execution mode for trade orders.
            - filling_mode (int): Order filling modes allowed.
            - order_mode (int): Modes of orders allowed.
            - select (bool): Specifies if the symbol is selected in the Market Watch window.
            - visible (bool): Indicates whether the symbol is visible in Market Watch.
            - custom (bool): Indicates whether the symbol is custom-created.
            - bidhigh (float): Highest Bid observed.
            - bidlow (float): Lowest Bid observed.
            - askhigh (float): Highest Ask observed.
            - asklow (float): Lowest Ask observed.
            - last (float): Last deal price.
            - lasthigh (float): Highest last deal price observed.
            - lastlow (float): Lowest last deal price observed.
            - volume (int): Volume of the last deal.
            - volume_real (float): Real volume of the last deal.
            - swap_long (float): Swap rate for long positions.
            - swap_short (float): Swap rate for short positions.
            - margin_initial (float): Initial margin requirement.
            - margin_maintenance (float): Maintenance margin requirement.
            - margin_hedged (float): Margin for hedged positions.
            - time (int): Time of the last quote as a Unix timestamp.
            - session_open (float): Session opening price.
            - session_close (float): Session closing price.
            - price_change (float): Price change over the session.
            - price_volatility (float): Price volatility.
            - category (str): Category of the symbol, e.g., Majors.
            - currency_margin (str): Margin currency of the symbol.
            - swap_rollover3days (int): Day of the week when triple swaps are applied.
            - trade_tick_value_profit (float): Tick value for profitable positions.
            - trade_tick_value_loss (float): Tick value for losing positions.
            - trade_calc_mode (int): Contract price calculation mode.
            - order_gtc_mode (int): Good-Till-Cancelled mode.
            - expiration_mode (int): Mode of expiration processing.
            - start_time (int): Date of the symbol trade beginning.
            - expiration_time (int): Date of the symbol trade end.
            - trade_stops_level (int): Minimal distance for Stop Loss/Take Profit.
            - trade_freeze_level (int): Modification block distance near market price.
            - session_deals (int): Number of deals in the current session.
            - session_volume (float): Session trading volume.
            - session_turnover (float): Session turnover value.
            - session_interest (float): Open interest in the session.
            - session_buy_orders (int): Number of Buy orders at the moment.
            - session_sell_orders (int): Number of Sell orders at the moment.
            - session_buy_orders_volume (float): Volume of buy orders in the session.
            - session_sell_orders_volume (float): Volume of sell orders in the session.
            - session_aw (float): Average weighted price for the session.
            - session_price_settlement (float): Settlement price of the session.
            - session_price_limit_min (float): Minimum allowed session price.
            - session_price_limit_max (float): Maximum allowed session price.
            - price_theoretical (float): Theoretical price (used in options).
            - price_greeks_delta (float): Option delta.
            - price_greeks_theta (float): Option theta.
            - price_greeks_gamma (float): Option gamma.
            - price_greeks_vega (float): Option vega.
            - price_greeks_rho (float): Option rho.
            - price_greeks_omega (float): Option omega.
            - price_sensitivity (float): Sensitivity of the price.
            - option_strike (float): Strike price for options.
            - option_mode (int): Option-specific setting.
            - option_right (int): Option type (call or put).
            - margin_hedged_use_leg (bool): If margin for hedged positions uses larger leg.
            - trade_accrued_interest (float): Accrued interest value.
            - trade_face_value (float): Face value of the contract.
            - trade_liquidity_rate (float): Liquidity rate.
            - volumehigh (int): Maximal day volume.
            - volumelow (int): Minimal day volume.
            - volumehigh_real (float): Highest real volume observed.
            - volumelow_real (float): Lowest real volume observed.
            - ticks_bookdepth (int): Depth of Market quote level count.
            - chart_mode (int): Defines the price type used for generating symbol bars.
            - swap_mode (int): Method of swap calculation.
            - bank (str): Associated bank (if any).
            - exchange (str): Associated exchange (if any).
            - formula (str): Pricing formula (if any).
            - isin (str): International Securities Identification Number.
            - basis (str): Basis of the symbol (if applicable).
            - page (str): Info page URL or reference.
            - path (str): Symbol path in Market Watch.
            
        Raises:
            SymbolNotFoundError: If symbol is invalid or not found.
            MarketError: If symbol information cannot be retrieved.
            ConnectionError: If not connected to terminal.
            
        Example:
            >>> market = MT5Market(connection)
            >>> eurusd_info = market.get_symbol_info("EURUSD")
            >>> print(f"EURUSD Bid: {eurusd_info['bid']}, Ask: {eurusd_info['ask']}")
            EURUSD Bid: 1.0921, Ask: 1.0923
        """
        
        # Try to get symbol information from MT5
        symbols = mt5.symbols_get(symbol_name)

        # Check if symbol exists
        if not symbols or len(symbols) == 0:
            raise SymbolNotFoundError(f"Symbol '{symbol_name}' not found")
            
        # Extract all non-callable attributes from the symbol object
        symbol_info = symbols[0]
        return {
            attr: getattr(symbol_info, attr) 
            for attr in dir(symbol_info) 
            if not attr.startswith('__') and not callable(getattr(symbol_info, attr))
        }
    
    def get_symbol_price(self, symbol_name: str) -> Dict[str, Any]:
        """
        Get current price for a symbol.
        
        Retrieves the latest price information for a specified symbol including bid, ask,
        and last deal prices. This is useful for getting real-time market data for
        price analysis, trade execution, or display purposes.
        
        Args:
            symbol_name: Symbol name (e.g., "EURUSD", "XAUUSD").
                         Must be an exact match to an existing symbol.
            
        Returns:
            Dict[str, Any]: Dictionary with price information:
                - bid (float): Current bid price (best sell offer)
                - ask (float): Current ask price (best buy offer)
                - last (float): Last deal price
                - volume (float): Volume for the current last price
                - time (datetime): Time of the last price update as datetime object in UTC timezone
                
        Raises:
            SymbolNotFoundError: If symbol is invalid or not found.
            MarketDataError: If price data cannot be retrieved.
            
        Example:
            >>> market = MT5Market(connection)
            >>> price_data = market.get_symbol_price("EURUSD")
            >>> print(f"Current EURUSD Bid: {price_data['bid']}, Ask: {price_data['ask']}")
            Current EURUSD Bid: 1.0921, Ask: 1.0923
        """

        # Get the latest tick data for the symbol
        tick = mt5.symbol_info_tick(symbol_name)
        
        # Check if tick data is available
        if tick is None:
            raise SymbolNotFoundError(f"Could not get price data for symbol '{symbol_name}'")
            
        # Convert tick time from Unix timestamp to datetime with UTC timezone
        tick_time = datetime.fromtimestamp(tick.time, tz=timezone.utc)
            
        # Return formatted price information
        return {
            "bid": tick.bid,
            "ask": tick.ask,
            "last": tick.last,
            "volume": tick.volume,
            "time": tick_time
        }
    
    def get_candles_latest(
        self,
        symbol_name: str,
        timeframe: str,
        count: int = 100
    ) -> pd.DataFrame:
        """
        Get the latest candles for a symbol as a pandas DataFrame.
        
        Retrieves the most recent price candles (OHLCV data) for a specified symbol
        and timeframe. This is useful for technical analysis, chart visualization,
        or algorithmic trading strategies that need recent price history.
        
        Args:
            symbol_name: Symbol name (e.g., "EURUSD", "XAUUSD").
                         Must be an exact match to an existing symbol.
            timeframe: Timeframe string (e.g., "M1", "H1"). Case-insensitive.
                       Common values:
                       - "M1", "M5", "M15", "M30" - minutes
                       - "H1", "H4" - hours
                       - "D1" - daily
                       - "W1" - weekly
                       - "MN1" - monthly
            count: Number of candles to retrieve (default: 100).
                   Maximum recommended value is 5000 for performance reasons.
            
        Returns:
            pd.DataFrame: DataFrame with OHLCV data:
                - time: Candle timestamp with UTC timezone
                - open: Open price
                - high: High price
                - low: Low price
                - close: Close price
                - tick_volume: Tick volume
                - spread: Spread
                - real_volume: Real volume (if available)
                
        Raises:
            SymbolNotFoundError: If symbol is invalid or not found.
            InvalidTimeframeError: If timeframe is invalid.
            MarketDataError: If candle data cannot be retrieved.
            ConnectionError: If not connected to terminal.
            
        Example:
            >>> market = MT5Market(connection)
            >>> # Get last 50 hourly candles for EURUSD
            >>> candles = market.get_candles_latest("EURUSD", "H1", 50)
            >>> print(f"Latest close price: {candles['close'].iloc[0]}")
            Latest close price: 1.0921
        """

        # Verify symbol exists
        if not self.get_symbols(symbol_name):
            raise SymbolNotFoundError(f"Symbol '{symbol_name}' not found")
        
        # Verify timeframe is valid
        tf = Timeframe.get(timeframe)
        if tf is None:
            raise InvalidTimeframeError(f"Invalid timeframe: '{timeframe}'")

        # Get candle data from MT5 (position 0 means starting from the most recent candle)
        candles = mt5.copy_rates_from_pos(symbol_name, tf, 0, count)
        
        # Check if data was successfully retrieved
        if candles is None or len(candles) == 0:
            raise MarketDataError(f"Failed to retrieve candle data for symbol '{symbol_name}' with timeframe '{timeframe}'")
        
        # Convert NumPy array to pandas DataFrame
        df = pd.DataFrame(candles)
        
        # Convert Unix timestamp to datetime with UTC timezone
        df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)
        
        # Sort by time in descending order (newest to oldest)
        df = df.sort_values('time', ascending=False)
        
        return df

    def get_candles_by_date(
        self, 
        symbol_name: str, 
        timeframe: str, 
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Get historical price data (OHLCV) for a symbol between specified dates.
        
        Retrieves historical candle data for a specified symbol and timeframe within
        a given date range. This method is ideal for backtesting trading strategies,
        performing historical analysis, or visualizing past market behavior.
        
        The method is flexible with date parameters:
        - If both dates are provided: returns data between those dates
        - If only from_date is provided: returns data from that date to the present (limited to 1000 candles)
        - If only to_date is provided: returns data for 30 days before that date
        - If no dates are provided: returns the most recent 1000 candles
        
        Args:
            symbol_name: Symbol name (e.g., "EURUSD", "XAUUSD").
                         Must be an exact match to an existing symbol.
            timeframe: Timeframe string (e.g., "M1", "H1"). Case-insensitive.
                       See get_candles_latest() for common values.
            from_date: Start date in "yyyy-MM-dd HH:mm" format in UTC (optional).
                       If None, depends on to_date parameter.
            to_date: End date in "yyyy-MM-dd HH:mm" format in UTC (optional).
                     If None, depends on from_date parameter.
            
        Returns:
            pd.DataFrame: DataFrame with OHLCV data sorted by newest to oldest:
                - time: Candle timestamp with UTC timezone
                - open: Open price
                - high: High price
                - low: Low price
                - close: Close price
                - tick_volume: Tick volume
                - spread: Spread
                - real_volume: Real volume (if available)
            
        Raises:
            SymbolNotFoundError: If symbol is invalid or not found.
            InvalidTimeframeError: If timeframe is invalid.
            MarketDataError: If historical data cannot be retrieved.
            ValueError: If date format is invalid or if to_date is earlier than from_date.
            
        Example:
            >>> market = MT5Market(connection)
            >>> # Get EURUSD hourly data for January 2023
            >>> candles = market.get_candles_by_date(
            ...     "EURUSD", 
            ...     "H1", 
            ...     "2023-01-01 00:00", 
            ...     "2023-01-31 23:59"
            ... )
            >>> print(f"Number of candles: {len(candles)}")
            Number of candles: 744
        """
        
        # Verify symbol exists
        if not self.get_symbols(symbol_name):
            raise SymbolNotFoundError(f"Symbol '{symbol_name}' not found")
        
        # Verify timeframe is valid
        tf = Timeframe.get(timeframe)
        if tf is None:
            raise InvalidTimeframeError(f"Invalid timeframe: '{timeframe}'")
            
        from_datetime = None
        to_datetime = None
        
        # Parse from_date if provided
        if from_date:
            try:
                from_datetime = datetime.strptime(from_date, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
            except ValueError:
                raise ValueError(f"Invalid from_date format: {from_date}. Expected format: 'yyyy-MM-dd HH:mm'")
        
        # Parse to_date if provided
        if to_date:
            try:
                to_datetime = datetime.strptime(to_date, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
            except ValueError:
                raise ValueError(f"Invalid to_date format: {to_date}. Expected format: 'yyyy-MM-dd HH:mm'")
        
        # Automatically swap dates if to_date is earlier than from_date
        if from_datetime and to_datetime and from_datetime > to_datetime:
            from_datetime, to_datetime = to_datetime, from_datetime
        
        candles = None
        
        # Case 1: Both from_date and to_date provided
        if from_datetime and to_datetime:
            candles = mt5.copy_rates_range(
                symbol_name, 
                tf, 
                from_datetime, 
                to_datetime
            )
        # Case 2: Only from_date provided
        elif from_datetime:
            candles = mt5.copy_rates_from(
                symbol_name, 
                tf, 
                from_datetime, 
                1000
            )
        # Case 3: Only to_date provided
        elif to_datetime:
            # Look back 30 days from the to_date
            lookback_days = 30
            start_date = to_datetime - timezone.timedelta(days=lookback_days)
            
            candles = mt5.copy_rates_range(
                symbol_name, 
                tf, 
                start_date, 
                to_datetime
            )
        # Case 4: No dates provided
        else:
            # Get recent candles (default behavior)
            candles = mt5.copy_rates_from_pos(
                symbol_name, 
                tf, 
                0, 
                1000  # Reasonable default limit
            )
        
        # Check if data was successfully retrieved
        if candles is None or len(candles) == 0:
            raise MarketDataError(f"Failed to retrieve historical data for symbol '{symbol_name}' with timeframe '{timeframe}'")
            
        # Convert NumPy array to pandas DataFrame
        df = pd.DataFrame(candles)
        
        # Convert Unix timestamp to datetime with UTC timezone
        df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)
        
        # Sort by time in descending order (newest to oldest)
        df = df.sort_values('time', ascending=False)
        
        return df