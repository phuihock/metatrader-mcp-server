"""
MetaTrader MCP Client package.

This package provides a modular interface for communicating with the MetaTrader 5 terminal.
"""

from .client import MT5Client
from .exceptions import (
    MT5ClientError, 
    ConnectionError, 
    OrderError, 
    MarketError,
    AccountError,
    HistoryError
)
from .orders import OrderType, OrderFilling, OrderTime

__all__ = [
    "MT5Client",
    "MT5ClientError",
    "ConnectionError",
    "OrderError",
    "MarketError",
    "AccountError",
    "HistoryError",
    "OrderType",
    "OrderFilling",
    "OrderTime"
]
