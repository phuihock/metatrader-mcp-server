"""
MetaTrader 5 order operations module.

This module handles trade execution, modification, and management.
"""

import pandas as pd
from typing import Optional, Union

from .functions.get_positions import get_positions
from .functions.get_pending_orders import get_pending_orders
from .functions.send_order import send_order


class MT5Orders:
	"""
	Handles MetaTrader 5 order operations.
	Provides methods to execute, modify, and manage trading orders.
	"""
	
	# ===================================================================================
	# Constructor
	# -----------------------------------------------------------------------------------
	# ✔ Done
	# ===================================================================================
	def __init__(self, connection):
		"""
		Initialize the order operations handler.
		
		Args:
			connection: MT5Connection instance for terminal communication.
		"""
		self._connection = connection
	

	# ===================================================================================
	# Get all open positions
	# -----------------------------------------------------------------------------------
	# ✔ Done
	# =================================================================================== 
	def get_all_positions(self) -> pd.DataFrame:
		"""
		Get all open positions across all symbols.
		
		Returns:
			pd.DataFrame: All open positions in a pandas DataFrame, ordered by time (descending).
		"""
		return get_positions(self._connection)


	# ===================================================================================
	# Get open positions by symbol
	# -----------------------------------------------------------------------------------
	# ✔ Done
	# =================================================================================== 
	def get_positions_by_symbol(self, symbol: str) -> pd.DataFrame:
		"""
		Get all open positions for a specific symbol.
		
		Args:
			symbol: The symbol name to filter positions by.
			
		Returns:
			pd.DataFrame: Open positions for the specified symbol in a pandas DataFrame, 
						  ordered by time (descending).
		"""
		return get_positions(self._connection, symbol_name=symbol)


	# ===================================================================================
	# Get open positions by currency
	# -----------------------------------------------------------------------------------
	# ✔ Done
	# =================================================================================== 
	def get_positions_by_currency(self, currency: str) -> pd.DataFrame:
		"""
		Get all open positions for a specific currency.
		
		Args:
			currency: The currency code to filter positions by (e.g., "USD", "EUR").
					 Will be formatted as "*currency*" for the group filter.
			
		Returns:
			pd.DataFrame: Open positions for the specified currency in a pandas DataFrame, 
						  ordered by time (descending).
		"""
		# Format currency with wildcards for the group filter
		currency_filter = f"*{currency}*"
		return get_positions(self._connection, group=currency_filter)


	# ===================================================================================
	# Get open positions by id
	# -----------------------------------------------------------------------------------
	# ✔ Done
	# =================================================================================== 
	def get_positions_by_id(self, id: Union[int, str]) -> pd.DataFrame:
		"""
		Get a specific open position by its ticket ID.
		
		Args:
			id: The ticket ID of the position to retrieve.
			
		Returns:
			pd.DataFrame: The position with the specified ticket ID in a pandas DataFrame.
						  Returns an empty DataFrame if no position with the given ID exists.
		"""
		return get_positions(self._connection, ticket=id)


	# ===================================================================================
	# Get all pending orders
	# -----------------------------------------------------------------------------------
	# ✔ Done
	# ===================================================================================
	def get_all_pending_orders(self) -> pd.DataFrame:
		"""
		Get all pending orders across all symbols.
		
		Returns:
			pd.DataFrame: All pending orders in a pandas DataFrame, ordered by time (descending).
		"""
		return get_pending_orders(self._connection)


	# ===================================================================================
	# Get pending orders by symbol
	# -----------------------------------------------------------------------------------
	# ✔ Done
	# ===================================================================================
	def get_pending_orders_by_symbol(self, symbol: str) -> pd.DataFrame:
		"""
		Get all pending orders for a specific symbol.
		
		Args:
			symbol: The symbol name to filter pending orders by.
			
		Returns:
			pd.DataFrame: Pending orders for the specified symbol in a pandas DataFrame, 
						  ordered by time (descending).
		"""
		return get_pending_orders(self._connection, symbol_name=symbol)


	# ===================================================================================
	# Get pending orders by currency
	# -----------------------------------------------------------------------------------
	# ✔ Done
	# ===================================================================================
	def get_pending_orders_by_currency(self, currency: str) -> pd.DataFrame:
		"""
		Get all pending orders for a specific currency.
		
		Args:
			currency: The currency code to filter pending orders by (e.g., "USD", "EUR").
					 Will be formatted as "*currency*" for the group filter.
			
		Returns:
			pd.DataFrame: Pending orders for the specified currency in a pandas DataFrame, 
						  ordered by time (descending).
		"""
		# Format currency with wildcards for the group filter
		currency_filter = f"*{currency}*"
		return get_pending_orders(self._connection, group=currency_filter)


	# ===================================================================================
	# Get pending orders by id
	# -----------------------------------------------------------------------------------
	# ✔ Done
	# ===================================================================================
	def get_pending_orders_by_id(self, id: Union[int, str]) -> pd.DataFrame:
		"""
		Get a specific pending order by its ticket ID.
		
		Args:
			id: The ticket ID of the pending order to retrieve.
			
		Returns:
			pd.DataFrame: The pending order with the specified ticket ID in a pandas DataFrame.
						  Returns an empty DataFrame if no pending order with the given ID exists.
		"""
		return get_pending_orders(self._connection, ticket=id)


	# ===================================================================================
	# Place market order (BUY or SELL)
	# -----------------------------------------------------------------------------------
	# ✦ On progress
	# ===================================================================================
	def place_market_order(self, type: str, symbol: str, volume: str):
		pass


	# ===================================================================================
	# Place pending order (BUY_LIMIT, SELL_LIMIT, BUY_STOP, SELL_STOP)
	# -----------------------------------------------------------------------------------
	# ✦ On progress
	# ===================================================================================
	def place_pending_order(self, type: str, symbol: str, volume: str, price: Union[float, int]):
		pass


	# ===================================================================================
	# Modify an open position
	# -----------------------------------------------------------------------------------
	# ✦ On progress
	# ===================================================================================
	def modify_position():
		pass


	# ===================================================================================
	# Modify a pending order
	# -----------------------------------------------------------------------------------
	# ✦ On progress
	# ===================================================================================
	def modify_pending_order():
		pass


	# ===================================================================================
	# Close an open position
	# -----------------------------------------------------------------------------------
	# ✦ On progress
	# ===================================================================================
	def close_position():
		pass


	# ===================================================================================
	# Cancel a pending order
	# -----------------------------------------------------------------------------------
	# ✦ On progress
	# ===================================================================================
	def cancel_pending_order():
		pass


	# ===================================================================================
	# Close all open positions
	# -----------------------------------------------------------------------------------
	# ✦ On progress
	# ===================================================================================
	def close_all_positions():
		pass


	# ===================================================================================
	# Close all open positions by symbol
	# -----------------------------------------------------------------------------------
	# ✦ On progress
	# ===================================================================================
	def close_all_positions_by_symbol():
		pass


	# ===================================================================================
	# Close all profittable positions
	# -----------------------------------------------------------------------------------
	# ✦ On progress
	# ===================================================================================
	def close_all_profittable_positions():
		pass


	# ===================================================================================
	# Close all losing positions
	# -----------------------------------------------------------------------------------
	# ✦ On progress
	# ===================================================================================
	def close_all_losing_positions():
		pass


	# ===================================================================================
	# Cancel all pending orders
	# -----------------------------------------------------------------------------------
	# ✦ On progress
	# ===================================================================================
	def cancel_all_pending_orders():
		pass


	# ===================================================================================
	# Cancel all pending orders by symbol
	# -----------------------------------------------------------------------------------
	# ✦ On progress
	# ===================================================================================
	def cancel_all_pending_orders_by_symbol():
		pass