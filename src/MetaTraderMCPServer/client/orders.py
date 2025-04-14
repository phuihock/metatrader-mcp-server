"""
MetaTrader 5 order operations module.

This module handles trade execution, modification, and management.
"""

import pandas as pd
from typing import Optional, Union

from MetaTraderMCPServer.client.market import MT5Market
from MetaTraderMCPServer.client.types.order_type import OrderType

from .types import TradeRequestActions

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
	# ✔ Done
	# ===================================================================================
	def place_market_order(self, type: str, symbol: str, volume: Union[float, int]):
		if type.upper() not in ["BUY", "SELL"]:
			return { "error": True, "message": f"Invalid type, should be BUY or SELL.", "data": None }
		response = send_order(
			self._connection,
			action=TradeRequestActions.DEAL,
			order_type=type,
			symbol=symbol,
			volume=volume,
		)
		if response["success"] is False:
			return { "error": True, "message": response["message"], "data": None }

		data = response["data"]
		return {
			"error": False,
			"message": f"{OrderType.to_string(data.request.type)} {data.request.symbol} {data.volume} LOT at {data.price} success [Position ID: {data.order}]",
			"data": response["data"]
		}


	# ===================================================================================
	# Place pending order (BUY_LIMIT, SELL_LIMIT, BUY_STOP, SELL_STOP)
	# -----------------------------------------------------------------------------------
	# ✔ Done
	# ===================================================================================
	def place_pending_order(
		self,
		*,
		type: str,
		symbol: str,
		volume: Union[float, int],
		price: Union[float, int],
		stop_loss: Optional[Union[float, int]] = 0.0,
		take_profit: Optional[Union[float, int]] = 0.0,
	):
		
		accepted_types  = ["BUY", "SELL"]
		if type not in accepted_types:
			return { "error": True, "message": f"Invalid type, should be BUY or SELL.", "data": None }
		
		market = MT5Market(self._connection)
		current_price = market.get_symbol_price(symbol_name=symbol)
		if current_price is None:
			return { "error": True, "message": f"Cannot get latest market price for {symbol}", "data": None }
		
		# Decide pending order type
		order_type = None
		price = float(price)
		if type == "BUY":
			order_type = "BUY_LIMIT" if current_price["ask"] > price else "BUY_STOP"
		else:
			order_type = "SELL_LIMIT" if current_price["bid"] < price else "SELL_STOP"

		response = send_order(
			self._connection,
			action = TradeRequestActions.PENDING,
			order_type = order_type,
			symbol = symbol,
			volume = float(volume),
			price = float(price),
			stop_loss = float(stop_loss),
			take_profit = float(take_profit),
		)

		if response["success"] is False:
			return { "error": True, "message": response["message"], "data": None }

		return {
			"error": False,
			"message": f"Place pending order {order_type} {symbol} {volume} LOT at {price} success [Order ID: {response["data"].order}]",
			"data": response["data"],
		}


	# ===================================================================================
	# Modify an open position
	# -----------------------------------------------------------------------------------
	# ✔ Done
	# ===================================================================================
	def modify_position(
		self,
		*,
		id: Union[str, int],
		stop_loss: Optional[Union[int, float]] = None,
		take_profit: Optional[Union[int, float]] = None,
	):
		position_id = None
		position_error = False
		position = None
		
		try:
			position_id = int(id)
		except ValueError:
			position_error = True

		if not position_error:
			positions = self.get_positions_by_id(position_id)
		if positions.index.size == 0:
			position_error = True
		else:
			position = positions.iloc[0]

		if position_error or position is None:
			return {
				"error": True,
				"message": f"Invalid position ID {id}",
				"data": None,
			}
		
		response = send_order(
			self._connection,
			action = TradeRequestActions.SLTP,
			position = position_id,
			stop_loss = stop_loss if stop_loss is not None else position["stop_loss"],
			take_profit = take_profit if take_profit is not None else position["take_profit"],
		)

		if response["success"] is False:
			return { "error": True, "message": response["message"], "data": None }

		return {
			"error": False,
			"message": f"Modify position {position_id} success, SL at {stop_loss}, TP at {take_profit}, current price {response["data"].price}",
			"data": response["data"],
		}

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
	# ✔ Done
	# ===================================================================================
	def close_position(self, id: Union[str, int]):
		position_id = None
		position_error = False
		position = None
		
		try:
			position_id = int(id)
		except ValueError:
			position_error = True

		if not position_error:
			positions = self.get_positions_by_id(position_id)
		if positions.index.size == 0:
			position_error = True
		else:
			position = positions.iloc[0]

		if position_error or position is None:
			return {
				"error": True,
				"message": f"Invalid position ID {id}",
				"data": None,
			}
		
		response = send_order(
			self._connection,
			action = TradeRequestActions.DEAL,
			position = position_id,
			order_type = "SELL" if position["type"] == "BUY" else "BUY",
			symbol = position["symbol"],
			volume = position["volume"],
		)

		if response["success"] is False:
			return { "error": True, "message": response["message"], "data": None }

		data = response["data"]
		return {
			"error": False,
			"message": f"Close position {position_id} success at price {data.price}",
			"data": response["data"]
		}


	# ===================================================================================
	# Cancel a pending order
	# -----------------------------------------------------------------------------------
	# ✔ Done
	# ===================================================================================
	def cancel_pending_order(self, *, id: Union[int, str]):
		order_id = None
		try:
			order_id = int(id)
		except ValueError:
			return {
				"error": True,
				"message": f"Invalid order ID {id}",
				"data": None,
			}
		
		response = send_order(
			self._connection,
			action = TradeRequestActions.REMOVE,
			order = order_id,
		)

		if response["success"] is False:
			return { "error": True, "message": response["message"], "data": None }

		data = response["data"]
		return {
			"error": False,
			"message": f"Cancel pending order {order_id} success",
			"data": data,
		}

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