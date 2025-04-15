"""
Order module functions for MetaTrader MCP Server client operations.
"""

from .get_positions import get_positions
from .get_pending_orders import get_pending_orders
from .calculate_margin import calculate_margin
from .calculate_profit import calculate_profit
from .calculate_price_targets import calculate_price_target
from .send_order import send_order
from .place_market_order import place_market_order
from .place_pending_order import place_pending_order

__all__ = [
    "get_positions", 
    "get_pending_orders", 
    "calculate_margin", 
    "calculate_profit",
    "calculate_price_target",
    "send_order",
    "place_market_order",
    "place_pending_order",
]
