"""
MetaTrader 5 order operations module.

This module handles trade execution, modification, and management.
"""

import pandas as pd
from typing import Optional, Union

from .market import MT5Market
from .types import TradeRequestActions
from .order import get_positions, get_pending_orders, send_order
from .order import place_market_order, place_pending_order


class MT5Orders:
	"""
	Handles MetaTrader 5 order operations.
	Provides methods to execute, modify, and manage trading orders.
	"""


	def __init__(self, connection):
		self._connection = connection
	

	def get_all_positions(self) -> pd.DataFrame:
		return get_positions(self._connection)


	def get_positions_by_symbol(self, symbol: str) -> pd.DataFrame:
		return get_positions(self._connection, symbol_name=symbol)


	def get_positions_by_currency(self, currency: str) -> pd.DataFrame:
		currency_filter = f"*{currency}*"
		return get_positions(self._connection, group=currency_filter)


	def get_positions_by_id(self, id: Union[int, str]) -> pd.DataFrame:
		return get_positions(self._connection, ticket=id)


	def get_all_pending_orders(self) -> pd.DataFrame:
		return get_pending_orders(self._connection)


	def get_pending_orders_by_symbol(self, symbol: str) -> pd.DataFrame:
		return get_pending_orders(self._connection, symbol_name=symbol)


	def get_pending_orders_by_currency(self, currency: str) -> pd.DataFrame:
		currency_filter = f"*{currency}*"
		return get_pending_orders(self._connection, group=currency_filter)


	def get_pending_orders_by_id(self, id: Union[int, str]) -> pd.DataFrame:
		return get_pending_orders(self._connection, ticket=id)


	def place_market_order(self, *, type: str, symbol: str, volume: Union[float, int]):
		return place_market_order(self._connection, type=type, symbol=symbol, volume=volume)
	
	
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
		
		return place_pending_order(
			self._connection,
			type=type,
			symbol=symbol,
			volume=volume,
			price=price,
			stop_loss=stop_loss,
			take_profit=take_profit,
		)


	def modify_position(
		self,
		id: Union[str, int],
		*,
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


	def modify_pending_order(
		self, *,
		id: Union[int, str],
		price: Optional[Union[int, float]] = None,
		stop_loss: Optional[Union[int, float]] = None,
		take_profit: Optional[Union[int, float]] = None,
	):

		order_id = None
		order = None

		try:
			order_id = int(id)
		except ValueError:
			return {
				"error": True,
				"message": f"Invalid order ID {id}",
				"data": None,
			}
		
		orders = get_pending_orders(
			self._connection,
			ticket = order_id
		)

		order = orders.iloc[0]
		if len(orders.iloc[0]) == 0:
			return {
				"error": True,
				"message": f"Invalid order ID {id}",
				"data": None,
			}

		price = price if price else float(order["open"])
		request = {
			"action": TradeRequestActions.MODIFY,
			"order": order_id,
			"price": price,
			"stop_loss": stop_loss,
			"take_profit": take_profit,
		}

		if stop_loss is None:
			del request["stop_loss"]
		if take_profit is None:
			del request["take_profit"]

		print(request)

		response = send_order(self._connection, **request)

		if response["success"] is False:
			return { "error": True, "message": response["message"], "data": None }

		data = response["data"]
		return {
			"error": False,
			"message": f"Modify pending order {order_id} success",
			"data": data,
		}


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


	def cancel_pending_order(self, id: Union[int, str]):
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


	def close_all_positions(self):
		positions = self.get_all_positions()
		count = 0
		for id in positions["id"]:
			self.close_position(id)
			count = count + 1
		return { "error": False, "message": f"Close {count} positions success", "data": None }


	def close_all_positions_by_symbol(self, symbol: str):
		positions = self.get_all_positions()
		positions = positions[positions["symbol"] == symbol]
		count = 0
		for id in positions["id"]:
			self.close_position(id)
			count = count + 1
		return { "error": False, "message": f"Close {count} {symbol} positions success", "data": None }


	def close_all_profittable_positions(self):
		positions = self.get_all_positions()
		positions = positions[positions["profit"] >= 0]
		count = 0
		for id in positions["id"]:
			self.close_position(id)
			count = count + 1
		return { "error": False, "message": f"Close {count} profittable positions success", "data": None }


	def close_all_losing_positions(self):
		positions = self.get_all_positions()
		positions = positions[positions["profit"] < 0]
		count = 0
		for id in positions["id"]:
			self.close_position(id)
			count = count + 1
		return { "error": False, "message": f"Close {count} losing positions success", "data": None }


	def cancel_all_pending_orders(self):
		pending_orders = self.get_pending_orders(self._connection)
		cancel_count = 0
		for id in pending_orders["id"]:
			self.cancel_pending_order(id)
			cancel_count = cancel_count + 1
		
		return { "error": False, "message": f"Cancel {cancel_count} pending orders success", "data": None }

		
	def cancel_pending_orders_by_symbol(self, symbol: str):
		pending_orders = self.get_pending_orders_by_symbol(symbol)
		cancel_count = 0
		for id in pending_orders["id"]:
			self.cancel_pending_order(id)
			cancel_count = cancel_count + 1
		
		return { "error": False, "message": f"Cancel {cancel_count} pending orders success", "data": None }