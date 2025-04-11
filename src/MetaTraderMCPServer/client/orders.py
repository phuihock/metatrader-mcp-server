"""
MetaTrader 5 order operations module.

This module handles trade execution, modification, and management.
"""

import MetaTrader5 as mt5
import pandas as pd
from typing import Optional, Union

from .market import MT5Market
from .utils import convert_positions_to_dataframe, convert_orders_to_dataframe
from .types import OrderType, OrderState, OrderFilling, OrderTime


class MT5Orders:
    """
    Handles MetaTrader 5 order operations.
    Provides methods to execute, modify, and manage trading orders.
    """
    
    # ===================================================================================
    # Constructor
    # -----------------------------------------------------------------------------------
    # Done
    # ===================================================================================
    def __init__(self, connection):
        """
        Initialize the order operations handler.
        
        Args:
            connection: MT5Connection instance for terminal communication.
        """
        self._connection = connection
    

    # ===================================================================================
    # Get open trade positions
    # -----------------------------------------------------------------------------------
    # Done
    # -----------------------------------------------------------------------------------
    # Argument rules:
    # - All arguments are optionals.
    # - If "ticket" is defined, then "symbol_name" and "group" will be ignored.
    # - If "symbol_name" is defined, then "group" will be ignored.
    # -----------------------------------------------------------------------------------
    # Returns trade positions in Panda's DataFrame, ordered by time (descending).
    # ===================================================================================
    def _get_positions(
        self,
        ticket: Optional[Union[int, str]] = None,
        symbol_name: Optional[str] = None,
        group: Optional[str] = None,
        order_type: Optional[Union[str, int, OrderType]] = None,
    ) -> pd.DataFrame:

        market = MT5Market(self._connection)
        
        # symbol_name and group validation
        if (ticket is not None):
            # Check if symbol_name is valid otherwise return empty DataFrame
            if symbol_name:
                symbols = market.get_symbols(symbol_name)
                if (len(symbols) != 1):
                    return pd.DataFrame()

            # Check if group is valid otherwise return empty DataFrame
            if group:
                symbols = market.get_symbols(group)
                if (len(symbols) == 0):
                    return pd.DataFrame()

        # Define result variable as DataFrame.
        result = pd.DataFrame()

        # Get positions using MetaTrader5 library
        positions = []
        if ticket is not None:
            # Convert ticket to integer if it's a string
            if isinstance(ticket, str):
                try:
                    ticket = int(ticket)
                except ValueError:
                    # Return empty DataFrame if ticket cannot be converted to int
                    return pd.DataFrame()
            
            positions = mt5.positions_get(ticket=ticket)
        elif symbol_name is not None:
            positions = mt5.positions_get(symbol=symbol_name)
        elif group is not None:
            positions = mt5.positions_get(group=group)
        else:
            positions = mt5.positions_get()

        # Convert positions to DataFrame with enhanced order types
        if positions is not None:
            result = convert_positions_to_dataframe(positions)
            
            # Filter by order_type if specified
            if order_type is not None and not result.empty:
                if isinstance(order_type, str):
                    type_code = OrderType.to_code(order_type)
                elif isinstance(order_type, OrderType):
                    type_code = order_type.value
                else:
                    type_code = order_type
                
                if 'type_code' in result.columns:
                    result = result[result['type_code'] == type_code]

        # Return result
        return result


    # ===================================================================================
    # Get pending orders
    # -----------------------------------------------------------------------------------
    # Done
    # -----------------------------------------------------------------------------------
    # Argument rules:
    # - All arguments are optionals.
    # - If "ticket" is defined, then "symbol_name" and "group" will be ignored.
    # - If "symbol_name" is defined, then "group" will be ignored.
    # -----------------------------------------------------------------------------------
    # Returns pending orders in Panda's DataFrame, ordered by time (descending).
    # ===================================================================================
    def _get_pending_orders(
        self,
        ticket: Optional[Union[int, str]] = None,
        symbol_name: Optional[str] = None,
        group: Optional[str] = None,
        order_type: Optional[Union[str, int, OrderType]] = None,
        order_state: Optional[Union[str, int, OrderState]] = None,
        order_filling: Optional[Union[str, int, OrderFilling]] = None,
        order_lifetime: Optional[Union[str, int, OrderTime]] = None,
    ) -> pd.DataFrame:
        market = MT5Market(self._connection)
        
        # symbol_name and group validation
        if (ticket is not None):
            # Check if symbol_name is valid otherwise return empty DataFrame
            if symbol_name:
                symbols = market.get_symbols(symbol_name)
                if (len(symbols) != 1):
                    return pd.DataFrame()

            # Check if group is valid otherwise return empty DataFrame
            if group:
                symbols = market.get_symbols(group)
                if (len(symbols) == 0):
                    return pd.DataFrame()

        # Define result variable as DataFrame.
        result = pd.DataFrame()

        # Get pending orders using MetaTrader5 library
        orders = []
        if ticket is not None:
            # Convert ticket to integer if it's a string
            if isinstance(ticket, str):
                try:
                    ticket = int(ticket)
                except ValueError:
                    # Return empty DataFrame if ticket cannot be converted to int
                    return pd.DataFrame()
            
            orders = mt5.orders_get(ticket=ticket)
        elif symbol_name is not None:
            orders = mt5.orders_get(symbol=symbol_name)
        elif group is not None:
            orders = mt5.orders_get(group=group)
        else:
            orders = mt5.orders_get()

        # Convert orders to DataFrame with enhanced order types
        if orders is not None:
            # Use the utility function to convert orders to DataFrame
            result = convert_orders_to_dataframe(orders)
            
            # Filter by order_type if specified
            if order_type is not None and not result.empty:
                if isinstance(order_type, str):
                    type_code = OrderType.to_code(order_type)
                elif isinstance(order_type, OrderType):
                    type_code = order_type.value
                else:
                    type_code = order_type
                
                if 'type_code' in result.columns:
                    result = result[result['type_code'] == type_code]
            
            # Filter by order_state if specified
            if order_state is not None and not result.empty:
                if isinstance(order_state, str):
                    state_code = OrderState.to_code(order_state)
                elif isinstance(order_state, OrderState):
                    state_code = order_state.value
                else:
                    state_code = order_state
                
                if 'state_code' in result.columns:
                    result = result[result['state_code'] == state_code]
                    
            # Filter by order_filling if specified
            if order_filling is not None and not result.empty:
                if isinstance(order_filling, str):
                    filling_code = OrderFilling.to_code(order_filling)
                elif isinstance(order_filling, OrderFilling):
                    filling_code = order_filling.value
                else:
                    filling_code = order_filling
                
                if 'filling_code' in result.columns:
                    result = result[result['filling_code'] == filling_code]
                    
            # Filter by order_lifetime if specified
            if order_lifetime is not None and not result.empty:
                if isinstance(order_lifetime, str):
                    lifetime_code = OrderTime.to_code(order_lifetime)
                elif isinstance(order_lifetime, OrderTime):
                    lifetime_code = order_lifetime.value
                else:
                    lifetime_code = order_lifetime
                
                if 'lifetime_code' in result.columns:
                    result = result[result['lifetime_code'] == lifetime_code]

        # Return result
        return result

    # def execute_trade(
    #     self, 
    #     symbol: str, 
    #     order_type: OrderType, 
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
    #         order_type: Type of order (BUY, SELL, etc.).
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
    #         Dict[str, Any]: Order result information including:
    #             - retcode: Operation return code
    #             - deal: Deal ticket if performed
    #             - order: Order ticket if placed
    #             - volume: Deal volume confirmed by broker
    #             - price: Deal price confirmed by broker
    #             - bid: Current bid price
    #             - ask: Current ask price
    #             - comment: Broker comment
            
    #     Raises:
    #         OrderError: If order execution fails.
    #         ConnectionError: If not connected to terminal.
    #     """
    #     pass
    
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
    #     Modify an existing order.
        
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
    #     pass
    
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
    #     pass
    
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
    #     pass
    
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
    #     pass
    
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
    #     pass
    
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
    #     pass
    
    # def calculate_margin(
    #     self,
    #     symbol: str,
    #     order_type: OrderType,
    #     volume: float,
    #     price: float
    # ) -> float:
    #     """
    #     Calculate margin required for a trade.
        
    #     Args:
    #         symbol: Symbol name.
    #         order_type: Type of order.
    #         volume: Trade volume in lots.
    #         price: Order price.
            
    #     Returns:
    #         float: Required margin amount.
            
    #     Raises:
    #         OrderError: If margin calculation fails.
    #         ConnectionError: If not connected to terminal.
    #     """
    #     pass
    
    # def calculate_profit(
    #     self,
    #     symbol: str,
    #     order_type: OrderType,
    #     volume: float,
    #     price_open: float,
    #     price_close: float
    # ) -> float:
    #     """
    #     Calculate profit for a trade.
        
    #     Args:
    #         symbol: Symbol name.
    #         order_type: Type of order.
    #         volume: Trade volume in lots.
    #         price_open: Opening price.
    #         price_close: Closing price.
            
    #     Returns:
    #         float: Expected profit amount.
            
    #     Raises:
    #         OrderError: If profit calculation fails.
    #         ConnectionError: If not connected to terminal.
    #     """
    #     pass
