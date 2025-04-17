#!/usr/bin/env python3
import os
import argparse
import logging

from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass

from metatrader_mcp.utils import init, get_client

# ────────────────────────────────────────────────────────────────────────────────
# 1) Lifespan context definition
# ────────────────────────────────────────────────────────────────────────────────
@dataclass
class AppContext:
	client: str

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:

	try:
		client = init(os.getenv("login"), os.getenv("password"), os.getenv("server"))
		yield AppContext(client=client)
	finally:
		client.disconnect()

# ────────────────────────────────────────────────────────────────────────────────
# 2) Instantiate FastMCP as `mcp` (must be named `mcp`, `server`, or `app`)
# ────────────────────────────────────────────────────────────────────────────────
mcp = FastMCP(
	"metatrader",
	lifespan=app_lifespan,
	dependencies=[],
)

# ────────────────────────────────────────────────────────────────────────────────
# 3) Register tools with @mcp.tool()
# ────────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def get_account_info(ctx: Context) -> dict:
	"""
	Get account information (balance, equity, profit, margin level, free margin, account type, leverage, currency).
	
	Returns:
		Dict with account info fields.
	"""
	client = get_client(ctx)
	return client.account.get_trade_statistics()

@mcp.tool()
def get_deals(ctx: Context, from_date: str = None, to_date: str = None, group: str = None, ticket: int = None, position: int = None) -> str:
	"""
	Get historical deals as CSV.
	
	Parameters:
		from_date (str, optional): Start date (ISO 8601 or 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM').
		to_date (str, optional): End date (ISO 8601 or 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM').
		group (str, optional): Filter by group name.
		ticket (int, optional): Filter by deal ticket number.
		position (int, optional): Filter by position ID.
	
	Returns:
		CSV string of deals.
	"""
	client = get_client(ctx)
	df = client.history.get_deals_as_dataframe(from_date=from_date, to_date=to_date, group=group, ticket=ticket, position=position)
	return df.to_csv() if hasattr(df, 'to_csv') else str(df)

@mcp.tool()
def get_orders(ctx: Context, from_date: str = None, to_date: str = None, group: str = None, ticket: int = None) -> str:
	"""
	Get historical orders as CSV.
	
	Parameters:
		from_date (str, optional): Start date (ISO 8601 or 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM').
		to_date (str, optional): End date (ISO 8601 or 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM').
		group (str, optional): Filter by group name.
		ticket (int, optional): Filter by order ticket number.
	
	Returns:
		CSV string of orders.
	"""
	client = get_client(ctx)
	df = client.history.get_orders_as_dataframe(from_date=from_date, to_date=to_date, group=group, ticket=ticket)
	return df.to_csv() if hasattr(df, 'to_csv') else str(df)

@mcp.tool()
def get_candles_by_date(ctx: Context, symbol_name: str, timeframe: str, from_date: str = None, to_date: str = None) -> str:
	"""
	Get candle data for a symbol in a given timeframe and date range as CSV.
	
	Parameters:
		symbol_name (str): Symbol name (e.g., 'EURUSD').
		timeframe (str): Timeframe string (e.g., 'M1', 'H1', 'D1').
		from_date (str, optional): Start date ('YYYY-MM-DD' or 'YYYY-MM-DD HH:MM').
		to_date (str, optional): End date ('YYYY-MM-DD' or 'YYYY-MM-DD HH:MM').
	
	Returns:
		CSV string of candles.
	"""
	client = get_client(ctx)
	df = client.market.get_candles_by_date(symbol_name=symbol_name, timeframe=timeframe, from_date=from_date, to_date=to_date)
	return df.to_csv() if hasattr(df, 'to_csv') else str(df)

@mcp.tool()
def get_candles_latest(ctx: Context, symbol_name: str, timeframe: str, count: int = 100) -> str:
	"""
	Get the latest N candles for a symbol and timeframe as CSV.
	
	Parameters:
		symbol_name (str): Symbol name (e.g., 'EURUSD').
		timeframe (str): Timeframe string (e.g., 'M1', 'H1', 'D1').
		count (int, optional): Number of candles to retrieve (default: 100).
	
	Returns:
		CSV string of candles.
	"""
	client = get_client(ctx)
	df = client.market.get_candles_latest(symbol_name=symbol_name, timeframe=timeframe, count=count)
	return df.to_csv() if hasattr(df, 'to_csv') else str(df)

@mcp.tool()
def get_symbol_info(ctx: Context, symbol_name: str) -> dict:
	"""
	Get info for a specific market symbol as a dictionary.
	
	Parameters:
		symbol_name (str): Symbol name (e.g., 'EURUSD').
	
	Returns:
		Dictionary of symbol info fields.
	"""
	client = get_client(ctx)
	return client.market.get_symbol_info(symbol_name=symbol_name)

@mcp.tool()
def get_symbol_price(ctx: Context, symbol_name: str) -> dict:
	"""
	Get the latest price info for a symbol as a dictionary.
	
	Parameters:
		symbol_name (str): Symbol name (e.g., 'EURUSD').
	
	Returns:
		Dictionary with price fields (bid, ask, last, volume, time).
	"""
	client = get_client(ctx)
	return client.market.get_symbol_price(symbol_name=symbol_name)

@mcp.tool()
def get_symbols(ctx: Context, group: str = None) -> list:
	"""
	Get a list of all available market symbols (optionally filter by group pattern).
	
	Parameters:
		group (str, optional): Filter symbols by group pattern (e.g., '*USD*').
	
	Returns:
		List of symbol names.
	"""
	client = get_client(ctx)
	return client.market.get_symbols(group=group)

# ────────────────────────────────────────────────────────────────────────────────
# Order module tools
# ────────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def get_positions(ctx: Context, symbol: str = None, ticket: int = None, magic: int = None) -> list:
	"""
	Get open positions (optionally filter by symbol, ticket, magic number).
	
	Parameters:
		symbol (str, optional): Symbol name to filter (e.g., 'EURUSD').
		ticket (int, optional): Position ticket ID.
		magic (int, optional): Magic number to filter.
	
	Returns:
		List of position dictionaries.
	"""
	client = get_client(ctx)
	return client.order.get_positions(symbol=symbol, ticket=ticket, magic=magic)

@mcp.tool()
def get_all_positions(ctx: Context) -> list:
	"""
	Get all open positions.
	
	Returns:
		List of all open position dictionaries.
	"""
	client = get_client(ctx)
	return client.order.get_all_positions()

@mcp.tool()
def get_positions_by_symbol(ctx: Context, symbol: str) -> list:
	"""
	Get open positions for a specific symbol.
	
	Parameters:
		symbol (str): Symbol name (e.g., 'EURUSD').
	
	Returns:
		List of position dictionaries for the symbol.
	"""
	client = get_client(ctx)
	return client.order.get_positions_by_symbol(symbol=symbol)

@mcp.tool()
def get_positions_by_currency(ctx: Context, currency: str) -> list:
	"""
	Get open positions for a specific currency.
	
	Parameters:
		currency (str): Currency code (e.g., 'USD').
	
	Returns:
		List of position dictionaries for the currency.
	"""
	client = get_client(ctx)
	return client.order.get_positions_by_currency(currency=currency)

@mcp.tool()
def get_positions_by_id(ctx: Context, ticket: int) -> list:
	"""
	Get open positions by ticket ID.
	
	Parameters:
		ticket (int): Position ticket ID.
	
	Returns:
		List of position dictionaries for the ticket.
	"""
	client = get_client(ctx)
	return client.order.get_positions_by_id(ticket=ticket)

@mcp.tool()
def get_pending_orders(ctx: Context, symbol: str = None, ticket: int = None, magic: int = None) -> list:
	"""
	Get pending orders (optionally filter by symbol, ticket, magic number).
	
	Parameters:
		symbol (str, optional): Symbol name to filter (e.g., 'EURUSD').
		ticket (int, optional): Order ticket ID.
		magic (int, optional): Magic number to filter.
	
	Returns:
		List of pending order dictionaries.
	"""
	client = get_client(ctx)
	return client.order.get_pending_orders(symbol=symbol, ticket=ticket, magic=magic)

@mcp.tool()
def get_all_pending_orders(ctx: Context) -> list:
	"""
	Get all pending orders.
	
	Returns:
		List of all pending order dictionaries.
	"""
	client = get_client(ctx)
	return client.order.get_all_pending_orders()

@mcp.tool()
def get_pending_orders_by_symbol(ctx: Context, symbol: str) -> list:
	"""
	Get pending orders for a specific symbol.
	
	Parameters:
		symbol (str): Symbol name (e.g., 'EURUSD').
	
	Returns:
		List of pending order dictionaries for the symbol.
	"""
	client = get_client(ctx)
	return client.order.get_pending_orders_by_symbol(symbol=symbol)

@mcp.tool()
def get_pending_orders_by_currency(ctx: Context, currency: str) -> list:
	"""
	Get pending orders for a specific currency.
	
	Parameters:
		currency (str): Currency code (e.g., 'USD').
	
	Returns:
		List of pending order dictionaries for the currency.
	"""
	client = get_client(ctx)
	return client.order.get_pending_orders_by_currency(currency=currency)

@mcp.tool()
def get_pending_orders_by_id(ctx: Context, ticket: int) -> list:
	"""
	Get pending orders by ticket ID.
	
	Parameters:
		ticket (int): Order ticket ID.
	
	Returns:
		List of pending order dictionaries for the ticket.
	"""
	client = get_client(ctx)
	return client.order.get_pending_orders_by_id(ticket=ticket)

@mcp.tool()
def calculate_margin(ctx: Context, symbol: str, volume: float, order_type: str, price: float = None, **kwargs) -> float:
	"""
	Calculate margin for an order.
	
	Parameters:
		symbol (str): Symbol name (e.g., 'EURUSD').
		volume (float): Lot size.
		order_type (str): Order type (e.g., 'buy', 'sell').
		price (float, optional): Order price (required for pending orders).
		**kwargs: Additional MetaTrader margin calculation parameters.
	
	Returns:
		Margin required (float).
	"""
	client = get_client(ctx)
	return client.order.calculate_margin(symbol=symbol, volume=volume, order_type=order_type, price=price, **kwargs)

@mcp.tool()
def calculate_profit(ctx: Context, symbol: str, volume: float, order_type: str, open_price: float, close_price: float, **kwargs) -> float:
	"""
	Calculate profit for a position or order.
	
	Parameters:
		symbol (str): Symbol name (e.g., 'EURUSD').
		volume (float): Lot size.
		order_type (str): Order type (e.g., 'buy', 'sell').
		open_price (float): Open price.
		close_price (float): Close price.
		**kwargs: Additional MetaTrader profit calculation parameters.
	
	Returns:
		Profit value (float).
	"""
	client = get_client(ctx)
	return client.order.calculate_profit(symbol=symbol, volume=volume, order_type=order_type, open_price=open_price, close_price=close_price, **kwargs)

@mcp.tool()
def calculate_price_target(ctx: Context, symbol: str, price: float, points: float = None, percent: float = None, **kwargs) -> dict:
	"""
	Calculate price targets for SL/TP.
	
	Parameters:
		symbol (str): Symbol name (e.g., 'EURUSD').
		price (float): Reference price.
		points (float, optional): Points distance for target.
		percent (float, optional): Percent distance for target.
		**kwargs: Additional calculation parameters.
	
	Returns:
		Dictionary with calculated price targets.
	"""
	client = get_client(ctx)
	return client.order.calculate_price_target(symbol=symbol, price=price, points=points, percent=percent, **kwargs)

@mcp.tool()
def send_order(ctx: Context, symbol: str, volume: float, order_type: str, price: float = None, sl: float = None, tp: float = None, comment: str = None, **kwargs) -> dict:
	"""
	Send a generic order.
	
	Parameters:
		symbol (str): Symbol name (e.g., 'EURUSD').
		volume (float): Lot size.
		order_type (str): Order type (e.g., 'buy', 'sell', 'buy_limit', etc).
		price (float, optional): Order price (for pending orders).
		sl (float, optional): Stop loss price.
		tp (float, optional): Take profit price.
		comment (str, optional): Order comment.
		**kwargs: Additional order parameters (expiration, magic, etc).
	
	Returns:
		Order result dictionary.
	"""
	client = get_client(ctx)
	return client.order.send_order(symbol=symbol, volume=volume, order_type=order_type, price=price, sl=sl, tp=tp, comment=comment, **kwargs)

@mcp.tool()
def place_market_order(ctx: Context, symbol: str, volume: float, order_type: str, sl: float = None, tp: float = None, comment: str = None, **kwargs) -> dict:
	"""
	Place a market order.
	
	Parameters:
		symbol (str): Symbol name (e.g., 'EURUSD').
		volume (float): Lot size.
		order_type (str): Order type ('buy' or 'sell').
		sl (float, optional): Stop loss price.
		tp (float, optional): Take profit price.
		comment (str, optional): Order comment.
		**kwargs: Additional order parameters (magic, etc).
	
	Returns:
		Order result dictionary.
	"""
	client = get_client(ctx)
	return client.order.place_market_order(symbol=symbol, volume=volume, order_type=order_type, sl=sl, tp=tp, comment=comment, **kwargs)

@mcp.tool()
def place_pending_order(ctx: Context, symbol: str, volume: float, order_type: str, price: float, sl: float = None, tp: float = None, expiration: str = None, comment: str = None, **kwargs) -> dict:
	"""
	Place a pending order.
	
	Parameters:
		symbol (str): Symbol name (e.g., 'EURUSD').
		volume (float): Lot size.
		order_type (str): Pending order type ('buy_limit', 'sell_stop', etc).
		price (float): Pending order price.
		sl (float, optional): Stop loss price.
		tp (float, optional): Take profit price.
		expiration (str, optional): Expiration date/time (ISO format).
		comment (str, optional): Order comment.
		**kwargs: Additional order parameters (magic, etc).
	
	Returns:
		Order result dictionary.
	"""
	client = get_client(ctx)
	return client.order.place_pending_order(symbol=symbol, volume=volume, order_type=order_type, price=price, sl=sl, tp=tp, expiration=expiration, comment=comment, **kwargs)

@mcp.tool()
def modify_position(ctx: Context, ticket: int, sl: float = None, tp: float = None, **kwargs) -> dict:
	"""
	Modify an open position by ticket ID.
	
	Parameters:
		ticket (int): Position ticket ID.
		sl (float, optional): New stop loss price.
		tp (float, optional): New take profit price.
		**kwargs: Additional modification parameters.
	
	Returns:
		Modification result dictionary.
	"""
	client = get_client(ctx)
	return client.order.modify_position(ticket=ticket, sl=sl, tp=tp, **kwargs)

@mcp.tool()
def modify_pending_order(ctx: Context, ticket: int, price: float = None, sl: float = None, tp: float = None, expiration: str = None, **kwargs) -> dict:
	"""
	Modify a pending order by ticket ID.
	
	Parameters:
		ticket (int): Pending order ticket ID.
		price (float, optional): New order price.
		sl (float, optional): New stop loss price.
		tp (float, optional): New take profit price.
		expiration (str, optional): New expiration (ISO format).
		**kwargs: Additional modification parameters.
	
	Returns:
		Modification result dictionary.
	"""
	client = get_client(ctx)
	return client.order.modify_pending_order(ticket=ticket, price=price, sl=sl, tp=tp, expiration=expiration, **kwargs)

@mcp.tool()
def close_position(ctx: Context, ticket: int, volume: float = None, price: float = None, **kwargs) -> dict:
	"""
	Close an open position by ticket ID.
	
	Parameters:
		ticket (int): Position ticket ID.
		volume (float, optional): Volume to close (default: all).
		price (float, optional): Closing price.
		**kwargs: Additional close parameters.
	
	Returns:
		Close result dictionary.
	"""
	client = get_client(ctx)
	return client.order.close_position(ticket=ticket, volume=volume, price=price, **kwargs)

@mcp.tool()
def cancel_pending_order(ctx: Context, ticket: int) -> dict:
	"""
	Cancel a pending order by ticket ID.
	
	Parameters:
		ticket (int): Pending order ticket ID.
	
	Returns:
		Cancel result dictionary.
	"""
	client = get_client(ctx)
	return client.order.cancel_pending_order(ticket=ticket)

@mcp.tool()
def close_all_positions(ctx: Context) -> dict:
	"""
	Close all open positions.
	
	Returns:
		Bulk close result dictionary.
	"""
	client = get_client(ctx)
	return client.order.close_all_positions()

@mcp.tool()
def close_all_positions_by_symbol(ctx: Context, symbol: str) -> dict:
	"""
	Close all open positions for a specific symbol.
	
	Parameters:
		symbol (str): Symbol name (e.g., 'EURUSD').
	
	Returns:
		Bulk close result dictionary.
	"""
	client = get_client(ctx)
	return client.order.close_all_positions_by_symbol(symbol=symbol)

@mcp.tool()
def close_all_profittable_positions(ctx: Context) -> dict:
	"""
	Close all profitable positions.
	
	Returns:
		Bulk close result dictionary.
	"""
	client = get_client(ctx)
	return client.order.close_all_profittable_positions()

@mcp.tool()
def close_all_losing_positions(ctx: Context) -> dict:
	"""
	Close all losing positions.
	
	Returns:
		Bulk close result dictionary.
	"""
	client = get_client(ctx)
	return client.order.close_all_losing_positions()

@mcp.tool()
def cancel_all_pending_orders(ctx: Context) -> dict:
	"""
	Cancel all pending orders.
	
	Returns:
		Bulk cancel result dictionary.
	"""
	client = get_client(ctx)
	return client.order.cancel_all_pending_orders()

@mcp.tool()
def cancel_pending_orders_by_symbol(ctx: Context, symbol: str) -> dict:
	"""
	Cancel all pending orders for a specific symbol.
	
	Parameters:
		symbol (str): Symbol name (e.g., 'EURUSD').
	
	Returns:
		Bulk cancel result dictionary.
	"""
	client = get_client(ctx)
	return client.order.cancel_pending_orders_by_symbol(symbol=symbol)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="MetaTrader MCP Server")
	parser.add_argument("--login",    type=str, help="MT5 login")
	parser.add_argument("--password", type=str, help="MT5 password")
	parser.add_argument("--server",   type=str, help="MT5 server name")
	
	args = parser.parse_args()

	# inject into lifespan via env vars
	if args.login:    os.environ["login"]    = args.login
	if args.password: os.environ["password"] = args.password
	if args.server:   os.environ["server"]   = args.server

	# run the MCP server (must call mcp.run)
	mcp.run(
		transport="stdio"
	)
