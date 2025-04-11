"""
MetaTrader 5 trade action definitions.

This module contains trade action type definitions for MetaTrader 5.
"""
from enum import Enum


class TradeAction(Enum):
    """
    Trading operation types supported by MetaTrader 5.
    
    Types:
        DEAL (1): Market order - immediate execution
        PENDING (5): Pending order - execution when conditions are met
        SLTP (6): Modify Stop Loss and Take Profit levels
        MODIFY (7): Modify parameters of existing order
        REMOVE (8): Delete order
        CLOSE_BY (10): Close position by an opposite one
    """
    DEAL = 1
    PENDING = 5
    SLTP = 6
    MODIFY = 7
    REMOVE = 8
    CLOSE_BY = 10
