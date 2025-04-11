"""
MetaTrader 5 order type definitions.

This module contains order type definitions and mappings for MetaTrader 5 constants.
"""
from enum import Enum


class OrderType(Enum):
    """
    Enhanced OrderType enumeration with bi-directional mapping capabilities.
    
    This combines the benefits of Python's Enum with dictionary-like lookups:
    - Access numeric values via OrderType.BUY, OrderType.SELL, etc. (Enum style)
    - Get string representation via OrderType.to_string(0) ("BUY")
    - Get numeric value via OrderType.to_code("BUY") (0)
    - Check if a code or name exists via OrderType.exists("BUY") or OrderType.exists(0)
    
    Examples:
        OrderType.BUY.value == 0
        OrderType.to_string(0) == "BUY"
        OrderType.to_code("BUY") == 0
        OrderType["BUY"].value == 0
    """
    BUY = 0
    SELL = 1
    BUY_LIMIT = 2
    SELL_LIMIT = 3
    BUY_STOP = 4
    SELL_STOP = 5
    BUY_STOP_LIMIT = 6
    SELL_STOP_LIMIT = 7
    CLOSE_BY = 8
    
    @classmethod
    def to_string(cls, code, default=None):
        """
        Convert numeric order type code to string representation.
        
        Args:
            code: Numeric order type code
            default: Value to return if code is not found
            
        Returns:
            str: String representation of order type or default value
        """
        for order_type in cls:
            if order_type.value == code:
                return order_type.name
        return default or f"UNKNOWN_{code}"
    
    @classmethod
    def to_code(cls, name, default=None):
        """
        Convert string order type name to numeric code.
        
        Args:
            name: String representation of order type
            default: Value to return if name is not found
            
        Returns:
            int: Numeric code for order type or default value
        """
        try:
            return cls[name.upper()].value
        except (KeyError, AttributeError):
            return default
    
    @classmethod
    def exists(cls, key):
        """
        Check if an order type code or name exists.
        
        Args:
            key: Order type code (int) or name (str)
            
        Returns:
            bool: True if the order type exists
        """
        if isinstance(key, int):
            return any(order_type.value == key for order_type in cls)
        elif isinstance(key, str):
            try:
                cls[key.upper()]
                return True
            except KeyError:
                return False
        return False
