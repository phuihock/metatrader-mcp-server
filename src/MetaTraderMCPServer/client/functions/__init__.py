"""
Function modules for MetaTrader MCP Server client operations.
"""

from .get_positions import get_positions
from .get_pending_orders import get_pending_orders
from .calculate_margin import calculate_margin
from .calculate_profit import calculate_profit
from .calculate_price_targets import calculate_price_target

__all__ = [
    "get_positions", 
    "get_pending_orders", 
    "calculate_margin", 
    "calculate_profit",
    "calculate_price_target"
]
