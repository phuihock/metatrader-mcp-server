"""
MetaTrader 5 history operations module.

This module handles historical deals, orders, and trading statistics.
"""
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime, timedelta
from enum import Enum
import logging
from time import time
import math

try:
    import MetaTrader5 as mt5
    import pandas as pd
    import numpy as np
except ImportError as e:
    if "MetaTrader5" in str(e):
        raise ImportError("MetaTrader5 package is not installed. Please install it with: pip install MetaTrader5")
    elif "pandas" in str(e):
        raise ImportError("pandas package is not installed. Please install it with: pip install pandas")
    elif "numpy" in str(e):
        raise ImportError("numpy package is not installed. Please install it with: pip install numpy")
    else:
        raise

from .exceptions import (
    HistoryError, 
    DealsHistoryError, 
    OrdersHistoryError, 
    StatisticsError, 
    ConnectionError
)

# Set up logger
logger = logging.getLogger("MT5History")


class DealType(Enum):
    """Deal types in MetaTrader 5."""
    BUY = 0           # Buy
    SELL = 1          # Sell
    BALANCE = 2       # Balance
    CREDIT = 3        # Credit
    CHARGE = 4        # Charge
    CORRECTION = 5    # Correction
    BONUS = 6         # Bonus
    COMMISSION = 7    # Commission
    COMMISSION_DAILY = 8  # Daily commission
    COMMISSION_MONTHLY = 9  # Monthly commission
    AGENT_COMMISSION = 10  # Agent commission
    INTEREST = 11     # Interest
    CANCELED_BUY = 12 # Canceled buy deal
    CANCELED_SELL = 13  # Canceled sell deal


class OrderState(Enum):
    """Order states in MetaTrader 5."""
    STARTED = 0       # Order started
    PLACED = 1        # Order placed
    CANCELED = 2      # Order canceled
    PARTIAL = 3       # Order partially executed
    FILLED = 4        # Order filled
    REJECTED = 5      # Order rejected
    EXPIRED = 6       # Order expired
    REQUEST_ADD = 7   # Order requested to add
    REQUEST_MODIFY = 8  # Order requested to modify
    REQUEST_CANCEL = 9  # Order requested to cancel


class MT5History:
    """
    Handles MetaTrader 5 history operations.
    
    Provides methods to retrieve historical deals, orders, and trading statistics.
    """
    
    def __init__(self, connection):
        """
        Initialize the history operations handler.
        
        Args:
            connection: MT5Connection instance for terminal communication.
        """
        self._connection = connection
        
        # Set up logging level based on connection's debug setting
        if getattr(self._connection, 'debug', False):
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
    
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
            List[Dict[str, Any]]: List of historical deals with properties:
                - ticket: Deal ticket
                - time: Deal execution time
                - type: Deal type
                - entry: Deal entry type (0-in, 1-out, 2-inout)
                - symbol: Symbol name
                - volume: Deal volume
                - price: Deal price
                - profit: Deal profit
                - commission: Deal commission
                - swap: Swap
                - fee: Fee
                - magic: Expert Advisor ID
                - position_id: Position identifier
                - order: Order ticket that triggered the deal
                - comment: Deal comment
            
        Raises:
            DealsHistoryError: If deals cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        # Check if connected to MT5
        if not self._connection.is_connected():
            raise ConnectionError("Not connected to MetaTrader 5 terminal.")
        
        # For history_deals_get, we need to use different approaches based on the parameters provided
        deals = None
        
        logger.debug(f"Retrieving deals with parameters: from_date={from_date}, to_date={to_date}, group={group}, ticket={ticket}, position={position}")
        
        try:
            # Case 1: Getting deals by ticket number
            if ticket is not None:
                logger.debug(f"Retrieving deals by ticket: {ticket}")
                deals = mt5.history_deals_get(ticket=ticket)
            
            # Case 2: Getting deals by position
            elif position is not None:
                logger.debug(f"Retrieving deals by position: {position}")
                deals = mt5.history_deals_get(position=position)
            
            # Case 3: Getting deals by date range (and optional group)
            else:
                # MT5 API requires both date parameters
                if from_date is None:
                    from_date = datetime.now() - timedelta(days=30)  # Default to last 30 days
                if to_date is None:
                    to_date = datetime.now()  # Default to current time
                
                logger.debug(f"Retrieving deals by date range: {from_date} to {to_date}")
                
                # If group is specified, include it as a keyword argument
                if group is not None:
                    deals = mt5.history_deals_get(from_date, to_date, group=group)
                else:
                    # Use positional arguments for dates
                    deals = mt5.history_deals_get(from_date, to_date)
        
        except Exception as e:
            error_code = -1
            if hasattr(mt5, 'last_error'):
                error = mt5.last_error()
                if error and len(error) > 1:
                    error_code = error[0]
            
            msg = f"Failed to retrieve deals history: {str(e)}"
            logger.error(msg)
            raise DealsHistoryError(msg, error_code)
        
        # Check if retrieval was successful
        if deals is None:
            error = mt5.last_error()
            msg = f"Failed to retrieve deals history: {error[1]}"
            logger.error(msg)
            raise DealsHistoryError(msg, error[0])
        
        # Check if deals were found
        if len(deals) == 0:
            logger.info("No deals found with the specified parameters.")
            return []
        
        # Convert deals tuple to list of dictionaries
        result = [deal._asdict() for deal in deals]
        logger.debug(f"Retrieved {len(result)} deals.")
        
        return result
    
    def get_orders(
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
            List[Dict[str, Any]]: List of historical orders with properties:
                - ticket: Order ticket
                - time_setup: Order setup time
                - time_done: Order execution time
                - time_expiration: Order expiration time
                - type: Order type
                - state: Order state
                - magic: Expert Advisor ID
                - position_id: Position identifier
                - symbol: Symbol name
                - volume_initial: Initial order volume
                - volume_current: Unfilled volume
                - price_open: Order price
                - sl: Stop Loss level
                - tp: Take Profit level
                - price_current: Current price
                - price_stoplimit: Stop Limit order price
                - comment: Order comment
            
        Raises:
            OrdersHistoryError: If orders cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        # Check if connected to MT5
        if not self._connection.is_connected():
            raise ConnectionError("Not connected to MetaTrader 5 terminal.")
        
        # For history_orders_get, we need to use different approaches based on the parameters provided
        orders = None
        
        logger.debug(f"Retrieving orders with parameters: from_date={from_date}, to_date={to_date}, group={group}, ticket={ticket}")
        
        try:
            # Case 1: Getting orders by ticket number
            if ticket is not None:
                logger.debug(f"Retrieving orders by ticket: {ticket}")
                orders = mt5.history_orders_get(ticket=ticket)
            
            # Case 2: Getting orders by date range (and optional group)
            else:
                # MT5 API requires both date parameters
                if from_date is None:
                    from_date = datetime.now() - timedelta(days=30)  # Default to last 30 days
                if to_date is None:
                    to_date = datetime.now()  # Default to current time
                
                logger.debug(f"Retrieving orders by date range: {from_date} to {to_date}")
                
                # If group is specified, include it as a keyword argument
                if group is not None:
                    orders = mt5.history_orders_get(from_date, to_date, group=group)
                else:
                    # Use positional arguments for dates
                    orders = mt5.history_orders_get(from_date, to_date)
        
        except Exception as e:
            error_code = -1
            if hasattr(mt5, 'last_error'):
                error = mt5.last_error()
                if error and len(error) > 1:
                    error_code = error[0]
            
            msg = f"Failed to retrieve orders history: {str(e)}"
            logger.error(msg)
            raise OrdersHistoryError(msg, error_code)
        
        # Check if retrieval was successful
        if orders is None:
            error = mt5.last_error()
            msg = f"Failed to retrieve orders history: {error[1]}"
            logger.error(msg)
            raise OrdersHistoryError(msg, error[0])
        
        # Check if orders were found
        if len(orders) == 0:
            logger.info("No orders found with the specified parameters.")
            return []
        
        # Convert orders tuple to list of dictionaries
        result = [order._asdict() for order in orders]
        logger.debug(f"Retrieved {len(result)} orders.")
        
        return result
    
    def get_total_deals(
        self,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> int:
        """
        Get total number of deals in history.
        
        Args:
            from_date: Start date for history (optional).
            to_date: End date for history (optional).
            
        Returns:
            int: Number of deals.
            
        Raises:
            DealsHistoryError: If deals count cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        # Check if connected to MT5
        if not self._connection.is_connected():
            raise ConnectionError("Not connected to MetaTrader 5 terminal.")
        
        # Log the request parameters
        logger.debug(f"Retrieving total deals count with parameters: from_date={from_date}, to_date={to_date}")
        
        # MT5 API requires both date parameters for history_deals_total
        # and they must be passed as positional arguments, not keyword arguments
        if from_date is None:
            from_date = datetime.now() - timedelta(days=30)  # Default to last 30 days
        if to_date is None:
            to_date = datetime.now()  # Default to current time
            
        # Get deals total with positional arguments
        total = mt5.history_deals_total(from_date, to_date)
        
        # Check if retrieval was successful
        if total is None:
            error = mt5.last_error()
            msg = f"Failed to retrieve deals count: {error[1]}"
            logger.error(msg)
            raise DealsHistoryError(msg, error[0])
        
        logger.debug(f"Retrieved total deals count: {total}")
        return total
    
    def get_total_orders(
        self,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> int:
        """
        Get total number of orders in history.
        
        Args:
            from_date: Start date for history (optional).
            to_date: End date for history (optional).
            
        Returns:
            int: Number of orders.
            
        Raises:
            OrdersHistoryError: If orders count cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        # Check if connected to MT5
        if not self._connection.is_connected():
            raise ConnectionError("Not connected to MetaTrader 5 terminal.")
        
        # Log the request parameters
        logger.debug(f"Retrieving total orders count with parameters: from_date={from_date}, to_date={to_date}")
        
        # MT5 API requires both date parameters for history_orders_total
        # and they must be passed as positional arguments, not keyword arguments
        if from_date is None:
            from_date = datetime.now() - timedelta(days=30)  # Default to last 30 days
        if to_date is None:
            to_date = datetime.now()  # Default to current time
            
        # Get orders total with positional arguments
        total = mt5.history_orders_total(from_date, to_date)
        
        # Check if retrieval was successful
        if total is None:
            error = mt5.last_error()
            msg = f"Failed to retrieve orders count: {error[1]}"
            logger.error(msg)
            raise OrdersHistoryError(msg, error[0])
        
        logger.debug(f"Retrieved total orders count: {total}")
        return total
    
    def get_deals_as_dataframe(
        self,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        group: Optional[str] = None,
        ticket: Optional[int] = None,
        position: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Get historical deals as a pandas DataFrame.
        
        Args:
            from_date: Start date for history (optional).
            to_date: End date for history (optional).
            group: Filter by group pattern, e.g., "*USD*" (optional).
            ticket: Filter by specific deal ticket (optional).
            position: Filter by position identifier (optional).
            
        Returns:
            pd.DataFrame: DataFrame of historical deals with time as index.
            
        Raises:
            DealsHistoryError: If deals cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        try:
            # Get deals as list of dictionaries
            deals = self.get_deals(from_date, to_date, group, ticket, position)
            
            # Return empty DataFrame if no deals
            if not deals:
                logger.info("No deals found, returning empty DataFrame.")
                return pd.DataFrame()
            
            # Create DataFrame from deals
            df = pd.DataFrame(deals)
            
            # Convert time column to datetime and set as index
            if 'time' in df.columns:
                df['time'] = pd.to_datetime(df['time'], unit='s')
                df.set_index('time', inplace=True)
            
            logger.debug(f"Created DataFrame with {len(df)} deals.")
            return df
            
        except DealsHistoryError:
            # Re-raise the original exception
            raise
        except Exception as e:
            # Handle any other exceptions during DataFrame creation
            msg = f"Error creating DataFrame from deals: {str(e)}"
            logger.error(msg)
            raise DealsHistoryError(msg)
    
    def get_orders_as_dataframe(
        self,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        group: Optional[str] = None,
        ticket: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Get historical orders as a pandas DataFrame.
        
        Args:
            from_date: Start date for history (optional).
            to_date: End date for history (optional).
            group: Filter by group pattern, e.g., "*USD*" (optional).
            ticket: Filter by specific order ticket (optional).
            
        Returns:
            pd.DataFrame: DataFrame of historical orders with time_setup as index.
            
        Raises:
            OrdersHistoryError: If orders cannot be retrieved.
            ConnectionError: If not connected to terminal.
        """
        try:
            # Get orders as list of dictionaries
            orders = self.get_orders(from_date, to_date, group, ticket)
            
            # Return empty DataFrame if no orders
            if not orders:
                logger.info("No orders found, returning empty DataFrame.")
                return pd.DataFrame()
            
            # Create DataFrame from orders
            df = pd.DataFrame(orders)
            
            # Convert time columns to datetime and set time_setup as index
            for col in ['time_setup', 'time_done', 'time_expiration']:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], unit='s')
            
            if 'time_setup' in df.columns:
                df.set_index('time_setup', inplace=True)
            
            logger.debug(f"Created DataFrame with {len(df)} orders.")
            return df
            
        except OrdersHistoryError:
            # Re-raise the original exception
            raise
        except Exception as e:
            # Handle any other exceptions during DataFrame creation
            msg = f"Error creating DataFrame from orders: {str(e)}"
            logger.error(msg)
            raise OrdersHistoryError(msg)
